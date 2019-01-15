import pandas as pd

#	Full File Path (w file + extension)
file_path = r"C:\Users\ARidding\Documents\Financials\Nov\November-FinancialReport.csv"

#	read CSV, title columns
raw_df = pd.read_csv(file_path, names=["Metrics", "Values"])

#	Totals
CLINIC_AR = raw_df.Values[raw_df["Metrics"]=="Clinic A/R"].values[0] #	CLINIC A/R

#	RADIOLOGY
RADIOLOGY_TAKING_REVENUE = raw_df[raw_df['Metrics'].str.contains("Taking")]["Values"].sum() #	RADIOLOGY TAKING REVENUE
RADIOLOGY_READING_REVENUE = raw_df[raw_df['Metrics'].str.contains("Reading")]["Values"].sum()#	RADIOLOGY READING REVENUE

#	Campus
CAMPUS_TREATMENT_REV = raw_df.Values[raw_df["Metrics"]=="Campus Clinic Treatment Revenue"].values[0]#	CAMPUS TREATMENT REV
ORTHOTICS_REVENUE = raw_df[(raw_df['Metrics'].str.contains("Orthotics") & (raw_df["Metrics"] != "Bronte Orthotics Rev") )]["Values"].sum()#	Orthotics
CAMPUS_MISCELLANIOUS = raw_df.Values[raw_df["Metrics"]=="Campus Clinic Miscellanious"].values[0] #	CAMPUS MISCELLANIOUS

#	Shockwave, Massage
SHOCKWAVE_REVENUE = raw_df.Values[(raw_df["Metrics"]=="Campus Clinic Shockwave Rev") | (raw_df["Metrics"]=="St. John's Shockwave Rev")| (raw_df["Metrics"]=="South Riverdale Shockwave Rev")].values[0].sum()#	Shockwave
RMT_REVENUE = raw_df[raw_df['Metrics'].str.contains("Massage")]["Values"].sum()#	RMT REVENUE

#	Bronte
BRONTE_TREATMENT_REVENUE = raw_df.Values[raw_df["Metrics"]=="Bronte Treatment Revenue"].values[0] #	BRONTE TREATMENT REVENUE 
BRONTE_ORTHOTICS = raw_df.Values[raw_df["Metrics"]=="Bronte Orthotics Rev"].values[0] #	BRONTE ORTHOTICS 
BRONTE_SHOCKWAVE = raw_df.Values[raw_df["Metrics"]=="Bronte Shockwave Rev"].values[0] #	BRONTE SHOCKWAVE 
BRONTE_MISCELLANEOUS = raw_df.Values[raw_df["Metrics"]=="Bronte Miscellanious"].values[0] #	BRONTE MISCELLANEOUS 

#	SR
SOUTH_RIVERDALE_TREATMENT_REV = raw_df.Values[raw_df["Metrics"]=="South Riverdale Treatment Revenue"].values[0] #	SOUTH RIVERDALE TREATMENT REV 
SOUTH_RIVERDALE_SHOCKWAVE = raw_df.Values[raw_df["Metrics"]=="South Riverdale Shockwave Rev"].values[0] #	SOUTH RIVERDALE SHOCKWAVE
SOUTH_RIVERDALE_MISCELLANEOUS = raw_df.Values[raw_df["Metrics"]=="South Riverdale Miscellanious"].values[0] #	SOUTH RIVERDALE MISCELLANEOUS

#	SHERBOURNE
SHERBOURNE_TREATMENT_REVENUE  = raw_df.Values[raw_df["Metrics"]=="Sherbourne Treatment Revenue"].values[0] #	SHERBOURNE TREATMENT REVENUE 
SHERBOURNE_SHOCKWAVE = raw_df.Values[raw_df["Metrics"]=="Sherbourne Shockwave Rev"].values[0] #	SHERBOURNE SHOCKWAVE
SHERBOURNE_MISCELLANEOUS = raw_df.Values[raw_df["Metrics"]=="Sherbourne Miscellanious"].values[0] #	SHERBOURNE MISCELLANEOUS

#	ST.J
ST_JOHNS_TREATMENT_REVENUE  = raw_df.Values[raw_df["Metrics"]=="St. John's Treatment Revenue"].values[0] #	ST. JOHN'S TREATMENT REVENUE 
ST_JOHNS_MISCELLANEOUS = raw_df.Values[raw_df["Metrics"]=="St. John's Miscellanious"].values[0] #	ST. JOHN'S MISCELLANEOUS

#	ACU
ACUPUNCTURE = raw_df[raw_df['Metrics'].str.contains("Acupuncture")]["Values"].sum()#	ACUPUNCTURE


#	Setup Data Dictionary
data = {"Clinic A/R":[raw_df.Values[raw_df["Metrics"]=="Clinic A/R"].values[0], 0],
		"BAD DEBT RECOVERY":[0, 0],
		"RADIOLOGY TAKING REVENUE":[0, RADIOLOGY_TAKING_REVENUE],
		"RADIOLOGY READING REVENUE":[0,RADIOLOGY_READING_REVENUE],
		"CAMPUS TREATMENT REVENUE":[0, CAMPUS_TREATMENT_REV],
		"ORTHOTICS REVENUE":[0,ORTHOTICS_REVENUE],
		"SHOCKWAVE":[0, SHOCKWAVE_REVENUE],
		"RMT REVENUE":[0, RMT_REVENUE],
		"CAMPUS MISCELLANEOUS":[0, CAMPUS_MISCELLANIOUS],
		"BRONTE TREATMENT REV":[0, BRONTE_TREATMENT_REVENUE],
		"BRONTE ORTHOTICS":[0, BRONTE_ORTHOTICS],
		"BRONTE SHOCKWAVE":[0, BRONTE_SHOCKWAVE],
		"BRONTE MISCELLANEOUS":[0, BRONTE_MISCELLANEOUS],
		"SOUTH RIVERDALE TREATMENT":[0, SOUTH_RIVERDALE_TREATMENT_REV],
		"SOUTH RIVERDALE SHOCKWAVE":[0, SOUTH_RIVERDALE_SHOCKWAVE],
		"SOUTH RIVERDALE MISCELLANEOUS":[0, SOUTH_RIVERDALE_MISCELLANEOUS],
		"SHERBOURNE TREATMENT REVENUE":[0, SHERBOURNE_TREATMENT_REVENUE],
		"SHERBOURNE SHOCKWAVE":[0, SHERBOURNE_SHOCKWAVE],
		"SHERBOURNE MISCELLANEOUS":[0, SHERBOURNE_MISCELLANEOUS],
		"ST. JOHN'S TREATMENT REVENUE":[0, ST_JOHNS_TREATMENT_REVENUE],
		"ST. JOHN'S MISCELLANEOUS":[0, ST_JOHNS_MISCELLANEOUS],
		"ACUPUNCTURE":[0, ACUPUNCTURE]}


final_report_df = pd.DataFrame.from_dict(data, orient='index', columns=["DEBIT","CREDIT"])
final_report_df.to_csv(r"C:\Users\ARidding\Documents\Financials\Nov\Journal Entry.csv")

if final_report_df.DEBIT.sum() == final_report_df.CREDIT.sum():
	print("DEBIT COLUMN: " + str(final_report_df.DEBIT.sum()))
	print("CREDIT COLUMN: " + str(final_report_df.CREDIT.sum()))
	print("ACCOUNTING GODS ARE HAPPY!")
else:
	print("DEBIT COLUMN: " + str(final_report_df.DEBIT.sum()))
	print("CREDIT COLUMN: " + str(final_report_df.CREDIT.sum()))
	print("ACCOUNTING GODS ARE SADDD")







