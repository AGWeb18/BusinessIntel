import pandas as pd
import glob
import os

#	Define the path to where the files are saved
file_path = r"//citrix3/OscarFileStorage/Anthony Reports/Accounting"
#	Incorporate the month to differentiate between reports
month = "October"

def newest_csv(path):
	#	Create function to identify the newest file in directory
	#	Utilize the created time
	list_of_files = glob.glob(path + "/*.csv") # * means all if need specific format then *.csv
	latest_file = max(list_of_files, key=os.path.getctime)
	return latest_file

def write_off_amount(df):
	#	Retrieve the Write Off total
	last_row = -1
	total = df.iloc[last_row,6]
	return total

def bad_debt_amount(df):
	#	Sum all the 'uncollectible'
	uncol = "uncollectible"
	write_off_subsection = df[df.iloc[:, 8]== uncol]
	return round(write_off_subsection["Write-Off"].sum(), 2)

#	Specific Location 
location_data = pd.read_csv(newest_csv(file_path), nrows=2)
specific_location = location_data.iloc[0, 1]
print(specific_location)

#	Read file into dataframe
raw_file = pd.read_csv(newest_csv(file_path), skiprows=4)

#	Setup totals here, utilize functions
write_off_total = write_off_amount(raw_file)
uncollectible_total = bad_debt_amount(raw_file)
leftover_amount = round(write_off_total - uncollectible_total, 2)

#	Setup the name of the metrics
name_leftover_amount = specific_location + "-Revenue Total"

#	If the program reads "All", then write datafrom  with new data. 
if specific_location == "All":
	#	Setup Dataframe if all clinics
	d = ({"Clinic A/R":[write_off_total],
	"Bad Debt":	[uncollectible_total]})

	df_write_off = pd.DataFrame.from_dict(d, orient='index')

	with open(r"C:\Users\ARidding\Documents\Financials\ " + month + "-df_write_off.csv", 'a') as f:
		df_write_off.to_csv(f, header=False, mode='a')

else:
	print(leftover_amount)
	d = ({specific_location + " Revenue Total": leftover_amount})
	df_write_off = pd.DataFrame.from_dict(d, orient='index')

	with open(r"C:\Users\ARidding\Documents\Financials\ " + month + "-df_write_off.csv", 'a') as f:
		df_write_off.to_csv(f, header=False, mode='a')
