
from sqlalchemy import create_engine
import pandas as pd
import pyodbc
import os
import numpy as np
from datetime import date
import logging
import dateutil.relativedelta

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', lambda x: f'{x:,.3f}') #  Applies formatting for Float values to 3 decimals. 
local_server_name = os.environ.get('local_server')
_PBI_table = os.environ.get('_PBI_table_local')
_ledger_DM = os.environ.get('_ledger_DM')

def get_current_month():
    return (date.today() + dateutil.relativedelta.relativedelta(months=-1)).strftime("%Y-%m")

def gen_GLAccountDF():
    engine = create_engine('mssql+pyodbc://' + local_server_name + '/' + _PBI_table + '?trusted_connection=yes&driver=SQL+Server+Native+Client+11.0')
    conn =engine.connect()
    gl_account_lookup = pd.read_sql_table(_ledger_DM, conn)
    gl_account_lookup.columns = ['CompanyCode','GLAccountNumber', 'Balance', 'Group', 'LineIfNegative', 'ZeroBalanceReporting']
    gl_account_lookup['GLAccountNumber'] = gl_account_lookup['GLAccountNumber'].astype(int)
    gl_account_lookup = gl_account_lookup[(gl_account_lookup['GLAccountNumber']<=3999) & (gl_account_lookup['CompanyCode']=='01')] 
    return gl_account_lookup

def date_convert(date_to_convert):
    tx_date = pd.to_datetime(date_to_convert)
    return tx_date.strftime("%Y-%m")

def gen_GLTransactions(tx_sql):
    engine = create_engine('mssql+pyodbc://' + local_server_name + '/' + 'JonasConstructionDM' + '?trusted_connection=yes&driver=SQL+Server+Native+Client+11.0') # Replace here
    conn =engine.connect()
    df = pd.read_sql_query(tx_sql, conn)
    df['MonthYear'] = df['TransactionDate'].apply(date_convert)
    df['GLAccountNumber'] = df['GLAccountNumber'].astype(int)
    return df

def write_to_sql(df, local_server_name):
    engine = create_engine('mssql+pyodbc://' + local_server_name + '/' + _PBI_table + '?trusted_connection=yes&driver=SQL+Server+Native+Client+11.0')
    conn =engine.connect()
    try:
        print('Writing to "BalanceSheet')
        df.to_sql('BalanceSheet',con=conn, if_exists='replace')
        print("Succes! Wrote {} rows to SQL".format(len(df)))
        return 'Success!'        
    except Exception as e:
        print(e)

month_year = get_current_month()

# #   Update Month Year Here ##############
# #########################################
# month_year = '2022-02'
# #########################################

tx_sql = "SELECT * FROM vwGL_AccountTransactions WHERE [CompanyCode] = '01'"
tx_archived = "SELECT * FROM [vwGL_AccountTransactionsArchived] WHERE [CompanyCode] = '01'"

#   Write into a DataFrame
GLAccontLookup = gen_GLAccountDF()
GLTransactions = gen_GLTransactions(tx_sql)
GLTransactions_archived = gen_GLTransactions(tx_archived)

#   Concat the archived and main GL table into 1 main
tx_df = pd.concat([GLTransactions,GLTransactions_archived])

#   Transform Data including Cumulative Sum
tx_df = tx_df.merge(GLAccontLookup, how='left', on='GLAccountNumber')

# #   We have 2 lists, this finds items which are present in 1 list and not the other.
# #   Filter GLAccount to work with missing elements. Will expand to n number of missing elements. 
missing_gl_accounts = [element for element in GLAccontLookup[GLAccontLookup['ZeroBalanceReporting'] == 'Y']['GLAccountNumber'].unique() if element not in tx_df['GLAccountNumber'].unique()] 
missing_glaccounts_df = GLAccontLookup[GLAccontLookup['GLAccountNumber'].isin(missing_gl_accounts)]
missing_glaccounts_df = pd.DataFrame(
                    {'CompanyCode_x': missing_glaccounts_df['CompanyCode'],
                    'GLAccountNumber': missing_glaccounts_df['GLAccountNumber'],
                    'GLDepartmentCode': '00',
                    'TransactionDate': date.today(),
                    'LineNumber': '',
                    'JournalType': '',
                    'Amount': 0,
                    'AuditNumber': '',
                    'CreatedDate': '',
                    'APSubledgerCode': '',
                    'MonthYear': month_year, 
                    'Balance': missing_glaccounts_df['Balance'], 
                    'Group': missing_glaccounts_df['Group'], 
                    'LineIfNegative': missing_glaccounts_df['LineIfNegative'], 
                    'ZeroBalanceReporting':missing_glaccounts_df['ZeroBalanceReporting']
                    })

tx_df = pd.concat([tx_df, missing_glaccounts_df], ignore_index = True, axis = 0)

#   `tx_df` now contains a very large dataset. Archived Trasactions + current Txs. 
#   Plus merged GLAccountLookup for additional columns
#   Now we begin to group by Account Number and by Month Year.
tx_df = tx_df.groupby(['GLAccountNumber','Balance','MonthYear']).agg({'Amount':sum,
                                                             'LineIfNegative':max,
                                                             }).reset_index()
                                                        
# #   Add a CumulativeAmount column for each group for all months. 
tx_df['CumulativeAmount'] = tx_df.groupby(['GLAccountNumber', 'Balance','LineIfNegative'])['Amount'].apply(lambda x: x.cumsum())

#   Solution for Gathering every GLAccountNumber regardless of MonthYear
pivot_df = pd.pivot_table(tx_df, index=['MonthYear','GLAccountNumber'],aggfunc=[np.sum])
pivot_df.columns = pivot_df.columns.droplevel() # Multi-level index removed here

export_df = pivot_df.unstack(level=1).fillna(0).stack(level=1).reset_index() #  Create a list of unique GLAccountsNums for every MonthYear
export_df = export_df.merge(GLAccontLookup, on='GLAccountNumber', how='left') # Left join on the pivot table to populate with GLAccountLookup DF

#   For each unique GLAccountNumber, Sum Each month into a cumulative amount column
#   Append into list and create a DF. 
d_from_df = []
for acc_num in list(export_df.GLAccountNumber.unique()):
    temp_df = export_df[export_df['GLAccountNumber'] == acc_num]
    temp_df['CumulativeAmount'] = round(temp_df['Amount'].cumsum(),2)
    d_from_df.append(temp_df)

balance_sheet = pd.concat(d_from_df)

# # ##################################################################################
#   Change the GLAccountNumber if the CumulativeAmount is negative. 
# # ##################################################################################
# balance_sheet.loc[balance_sheet['CumulativeAmount'] < 0 , 'Group W Negative'] = balance_sheet['LineIfNegative']
# balance_sheet.loc[balance_sheet['CumulativeAmount'] >= 0 , 'Group W Negative'] = balance_sheet['GLAccountNumber']

balance_sheet['GLAccountNumber'] = balance_sheet['GLAccountNumber'].astype(str)
balance_sheet['GroupDescription'] = balance_sheet['GLAccountNumber'] +'-'+ balance_sheet['Balance']
balance_sheet['GLAccountNumber'] = balance_sheet['GLAccountNumber'].astype(int)
balance_sheet['MonthYear']= pd.to_datetime(balance_sheet['MonthYear'], format="%Y-%m")

# #   Replace any NA's in "Credit" with 0. 
balance_sheet.loc[balance_sheet.CumulativeAmount < 0, 'Credit'] = balance_sheet.CumulativeAmount
balance_sheet['Credit'] = balance_sheet['Credit'].fillna(0)

#   Create a new column based on conditional - adds "Asset / Liability / Equity" label. 
conditions = [
    ((balance_sheet['GLAccountNumber'] >= 1000) & (balance_sheet['GLAccountNumber'] <= 1999)),
    ((balance_sheet['GLAccountNumber'] >= 2000) & (balance_sheet['GLAccountNumber'] <= 2999)),
    ((balance_sheet['GLAccountNumber'] >= 3000) & (balance_sheet['GLAccountNumber'] <= 3999)),
    (balance_sheet['GLAccountNumber'] > 3999)
    ]
# create a list of the values we want to assign for each condition
values = ['1 - Asset', '2 - Liability', '3 - Equity', '4 - Other']

# create a new column and use np.select to assign values to it using our lists as arguments
balance_sheet['ItemType'] = np.select(conditions, values)
balance_sheet = balance_sheet[(balance_sheet['ItemType'] == '1 - Asset') | (balance_sheet['ItemType'] == '2 - Liability') | (balance_sheet['ItemType'] ==  '3 - Equity')]
balance_sheet['LoadDate'] = date.today()

# ####
# #   Option to write as a CSV
# ####
# # balance_sheet[balance_sheet['MonthYear']==month_year].to_csv("Balance Sheet -" + str(month_year) + ".csv")

# ####
# #   Option to write as in SQL 
# ####
# write_to_sql(balance_sheet, local_server_name)