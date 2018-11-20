#   Use this script to produce a report of each interns activity.
#   Begin with a single metric to ensure the methodology is sound.

#######################################################################
#	Follow up Questions:
#	Do Students/Staff count? STD NC or STF sub count
#######################################################################

#######################################################################
#	Two dataframes - one used for counting, one used for storing
#	counting = full dataset, groupped ---- intern_activity ------
#	storing = deduped df, with extra columns ---intern_activity_deduped---

######################### PRE-PROCESSING ##############################
#######################################################################

#   Import required libraries
import pandas as pd

pd.set_option('display.max_columns', 10) #	Set to 10 columns viewable

#   Read the csv into a dataframe
raw_file = pd.read_csv(r"\\citrix3\OscarFileStorage\Anthony Reports\Benchmark - Reports\July2018-ProviderDetailReport.csv")

#   Remove unnecessary columns
raw_file = raw_file[["Invoice ID", "Date", "Provider", "Procedure"]]

#   Keep rows with a '/' (those with an intern)
#	Split off procedure/date information into new df
intern_data = raw_file[raw_file.Provider.str.contains("/", na=False)]

#	name the cols of the procedure/date df. 
intern_procedure_codes = raw_file[["Invoice ID", "Procedure", "Date"]]

#   Split interns into multiple columns by "/"
only_intern_df = intern_data["Provider"].str.split('/', expand=True)

only_intern_df = only_intern_df[[1,2, 3]] #    Drop the clinician, keep interns
only_intern_df.columns = ["Intern1", "Intern2", "Intern3"] #	Rename column

#   Attach intern columns back to the date / procedure df
intern_activity = pd.concat([only_intern_df, intern_procedure_codes],axis=1, join='inner')

#	Fill NA's with "" in order to concatenate
intern_activity.Intern2.fillna(value="", inplace=True)
intern_activity.Intern3.fillna(value="", inplace=True)

intern_activity.columns = ["Intern1", "Intern2", "Intern3","InvoiceID","Procedure","Date"]

########################################################################################################################
#	Mapping procedure codes to their meaning. 
procedure_code_mapping = {"6100 NC":"NP", "6100 Reeval - NP credit":"NP", "Bronte Reeval NP credit":"NP", 
"GLAD CMCC NP":"NP", "GLAD NP":"NP","IB Bronte":"NP","IB INIT":"NP", "IB Outreach":"NP",
 "IB Sherb":"NP", "IB STJ":"NP", "Sher Reeval - NP credit":"NP",
"SRV initial":"NP", "SRV Reeval - NP credit":"NP", "STJ Reeval - NP credit":"NP",
"WSIB initial":"NP", "MIG initial":"NP","GLAD sub":"SUB",
"IB Bronte reeval":"SUB", "IB NC":"SUB","IB REEVAL":"SUB",
"IB Sherb reeval":"SUB","IB SRV reeval":"SUB","IB STJ NC":"SUB","IB STJ Re Eval":"SUB",
"SB Bronte":"SUB","SB Extended":"SUB","SB HR sub":"SUB", "SB no show":"SUB",
"SB one hour":"SUB", "SB OT":"SUB", "SB OT return":"SUB","SB Outreach MACC":"SUB",
"SB Sherb":"SUB","SB STJ":"SUB","SB SUB":"SUB", "SB TXIN":"SUB", "SRV sub":"SUB",
"SB POC Sub":"SUB", "WSIB sub":"SUB","MIG sub":"SUB","ADJ CER":"SMT", "ADJ LUM":"SMT","ADJ PEL":"SMT", "ADJ THOR":"SMT",
"MOBS CER":"SMT", "MOBS LUM":"SMT","MOBS PEL":"SMT","MOBS THR":"SMT",
"MOBS ANK":"EXT-SMT","MOBS ELB":"EXT-SMT","MOBS FT":"EXT-SMT","MOBS HIP":"EXT-SMT",
"MOBS HND":"EXT-SMT","MOBS KNE":"EXT-SMT","MOBS RIB":"EXT-SMT","MOBS SHD":"EXT-SMT",
"MOBS TMJ":"EXT-SMT", "ADJ ANK":"EXT-SMT", "ADJ ELB":"EXT-SMT","ADJ FT":"EXT-SMT",
"ADJ":"EXT-SMT", "ADJ KNEE":"EXT-SMT", "ADJ RIB":"EXT-SMT", "ADJ SHD":"EXT-SMT", 
"ADJ TMJ":"EXT-SMT","ADJ WRT":"EXT-SMT","AJD HIP":"EXT-SMT"}
#########################################################################################################################

#	Create the de-duped Interns Workbook df
master_df = intern_activity.drop_duplicates(subset=["Intern1","Intern2","Intern3"])


#	Add empty columns for new patient, subs, smt and external smt
master_df["NSTD NP"] = ""
master_df["STD NP"] = ""
master_df["NSTD SUBS"] = ""
master_df["STD SUBS"] = ""
master_df["NSTD SMT"] = ""
master_df["NSTD SMT"] = ""
master_df["NSTD EXT-SMT"] = ""
master_df["STD EXT-SMT"] = ""



###########################################################################################
#	Create function to count the number of important metrics for each data point
#def count_metrics(df_groupby):
	#	de-dupe the procedure codes
	#	map the Procedure to it's corresponding value
	#	count 1 of each of the important metrics per group if present. 
	#	place each important metrics into their own columns. 
###########################################################################################

activity_group = intern_activity.groupby(["InvoiceID"])

for key, val in activity_group:
	if val["Procedure"].contains 