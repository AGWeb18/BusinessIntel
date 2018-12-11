import pandas as pd
import os
import glob

file_path = r"//citrix3/OscarFileStorage/Anthony Reports/Accounting"

def newest_csv(path):
	#	Create function to identify the newest file in directory
	#	Utilize the created time
	list_of_files = glob.glob(path + "/*.csv") # * means all if need specific format then *.csv
	latest_file = max(list_of_files, key=os.path.getctime)
	return latest_file

def debit_amount(df):
	#	Calculate the initial total amount
	total_df = df.iloc[15, 3]
	acc_entries = df.iloc[0, 3]
	debit_amount_total = total_df - acc_entries
	return debit_amount_total

def treatment_rev(df):
	#	Function to calculate the treatment rev
	positive_vals = [4, 9, 13, 14]
	negative_vals = [3]
	pos_df = df.iloc[positive_vals,3].sum()
	neg_df = df.iloc[negative_vals, 3].sum()
	treatment_val = pos_df + neg_df
	return treatment_val

def orthotics_rev(df):
	#	Calculate the orthotics revenue
	positive_orth_vals = [2, 7]
	pos_orth_df = df.iloc[positive_orth_vals, 3].sum()
	return pos_orth_df

def misc_rev(df):
	#	Calculate Miscellanious rev
	positive_misc_vals = [6]
	pos_misc_df = df.iloc[positive_misc_vals, 3].sum()
	return pos_misc_df	

def shock_rev(df):
	#	Calculate Shockwave rev
	positive_shock_vals = [8]
	pos_shock_df = df.iloc[positive_shock_vals, 3].sum()
	return pos_shock_df

def acupuncture_rev(df):
	#	Calculate Acupuncture rev
	positive_acu_vals = [1]
	pos_acu_df = df.iloc[positive_acu_vals, 3].sum()
	return pos_acu_df	

def rmt_rev(df):
	#	Calculate Acupuncture rev
	positive_rmt_vals = [5]
	pos_rmt_df = df.iloc[positive_rmt_vals, 3].sum()
	return pos_rmt_df	

def radiology(df):
	#	Calculate Radiology Reading and Taking
	rad_taking = [11]
	rad_taking_df = df.iloc[rad_taking, 3].sum()
	rad_reading = [10]
	rad_reading_df = df.iloc[rad_reading, 3].sum()
	return rad_taking_df, rad_reading_df


#	Specific Location 
location_data = pd.read_csv(newest_csv(file_path), nrows=2)
specific_location = location_data.iloc[0, 1]
print(specific_location)

#	Read file into dataframe
raw_file = pd.read_csv(newest_csv(file_path), skiprows=4)


if specific_location == "All":
	#	Clinic A/R
	name_total = "Clinic A/R"
	val_total = round(debit_amount(raw_file), 2)
	d = {name_total:[val_total]}

	df_financial = pd.DataFrame.from_dict(d, orient="index")	

	with open(r"C:\Users\ARidding\Documents\Financials\financial_working.csv", 'a') as f:
		df_financial.to_csv(f, header=False, mode='a') 



else:
	name_treatment_rev = str(specific_location) + " Treatment Revenue"
	val_treatment_rev = round(treatment_rev(raw_file), 2)

	name_orth_rev = str(specific_location) + " Orthotics Rev"
	val_orth_rev = round(orthotics_rev(raw_file), 2)

	name_misc_rev = str(specific_location) + " Miscellanious"
	val_misc_rev = round(misc_rev(raw_file), 2)

	name_shock_rev = str(specific_location) + " Shockwave Rev"
	val_shock_rev = round(shock_rev(raw_file), 2)

	name_acu_rev = (str(specific_location) + " Acupuncture")
	val_acu_rev = round(acupuncture_rev(raw_file), 2)

	name_msg_rev = (str(specific_location) + " Massage Therapy")
	val_msg_rev = round(rmt_rev(raw_file), 2)

	name_rad_take = (str(specific_location) +" Radiology Taking")
	val_rad_take = round(radiology(raw_file)[0], 2)

	name_rad_read = (str(specific_location) +" Radiology Reading")
	val_rad_read = round(radiology(raw_file)[1], 2)

	d = ({name_treatment_rev:[val_treatment_rev], 
			name_orth_rev:[val_orth_rev], 
			name_misc_rev:[val_misc_rev], 
			name_shock_rev:[val_shock_rev],
			name_acu_rev:[val_acu_rev],
			name_msg_rev:[val_msg_rev],
			name_rad_take:[val_rad_take],
			name_rad_read:[val_rad_read]})

	df_financial = pd.DataFrame.from_dict(d, orient="index")


	with open(r"C:\Users\ARidding\Documents\Financials\financial_working.csv", 'a') as f:
		df_financial.to_csv(f, header=False, mode='a') 