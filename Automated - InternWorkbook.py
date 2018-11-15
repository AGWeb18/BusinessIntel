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
#######################################################################

#   Import required libraries
import pandas as pd
import re, string

pd.set_option('display.max_columns', 10) #	Set to 10 columns

#   Read the csv into a dataframe
raw_file = pd.read_csv(r"C:\Users\ARidding\Documents\Benchmarks\BarComparison\June2018-ProviderDetailReport.csv")

#   Remove unnecessary columns
raw_file = raw_file[["Date", "Provider", "Procedure"]]

#   Keep rows with a '/'.
#	Split off procedure/date information
intern_data = raw_file[raw_file.Provider.str.contains("/", na=False)]
intern_procedure_codes = raw_file[["Procedure", "Date"]]

#   Split interns into multiple columns
only_intern_df = intern_data["Provider"].str.split('/', expand=True)
only_intern_df = only_intern_df[[1,2]] #    Drop the clinician, keep interns
only_intern_df.columns = ["Intern1", "Intern2"] #	Rename column

#   Attach intern columns back to the dataframe
intern_activity = pd.concat([only_intern_df, intern_procedure_codes],axis=1, join='inner')
intern_activity = intern_activity[["Intern1","Intern2","Date","Procedure"]]


#	Create key to align the records
intern_activity["key"] = intern_activity["Date"] + intern_activity["Intern1"] + intern_activity["Intern2"]


#	Dedupe the dataframe, keep 1 item per 'group'
intern_activity_deduped = intern_activity.drop_duplicates(subset=["Date","Intern1", "Intern2"])

print(intern_activity_deduped.head())

#	Create Regex to remove all non-alpha numeric for key creation
pattern = re.compile(r'[\W_]+')

#	Add empty columns for new patient, subs, smt and external smt
intern_activity_deduped["NP"] = ""
intern_activity_deduped["SUBS"] = ""
intern_activity_deduped["SMT"] = ""
intern_activity_deduped["EXT-SMT"] = ""
intern_activity_deduped["key"] = ""


#	Reset index to make working with df easier
#intern_activity_deduped.reset_index(drop=True, inplace=True)

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

#	Instantiate empty dataframe for the count exercise

#	Groupby the date, and both interns. 
#intern_activity_group = intern_activity.groupby(by=["Date","Intern1","Intern2"])

#def create_key(item):
#	concat_item = item.iloc[2,0] + value["Intern1"].iloc[0] + value["Intern2"].iloc[0] #	Create key to use as a 'look-up'
#	value_concat= pattern.sub('', value_concat)
	




#for key, value  in intern_activity_group:
#	value_concat = value["Date"].iloc[0] + value["Intern1"].iloc[0] + value["Intern2"].iloc[0] #	Create key to use as a 'look-up'
#	value_concat= pattern.sub('', value_concat)
#	value["key"] = value_concat
#	print(value.head())
#	s_metrics = pd.Series(value["Procedure"].map(procedure_code_mapping).unique())
		

###########################################################################################
#	Create function to count the number of important metrics for each data point
#def count_metrics(df_groupby):
	#	de-dupe the procedure codes
	#	map the Procedure to it's corresponding value
	#	count 1 of each of the important metrics per group if present. 
	#	place each important metrics into their own columns. 
###########################################################################################


#	Produce a unique list of interns across the entire month
#l_of_interns = pd.concat([only_intern_df["Intern1"], only_intern_df['Intern2']]) #	List of interns

