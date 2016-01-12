import pandas as pd
import numpy as np
from datetime import datetime
'''
df1 = transaction data
df2 = duration of time spent on activity by day
'''
path = "C:\Users\WilliamLaptop\Desktop\QS DataFiles\{}"
path2 = "C:\Users\Bill\Google Drive\Finance{}"
#path = "C:\Users\Bill\Google Drive\Finance\{}"
finance_files = ["transactions2014.csv",
			"transactions2015_1.csv",
			"transactions2015_2.csv"]
			
frames = [pd.read_csv(path.format(x)) for x in finance_files]
df1 = pd.concat(frames).reset_index(drop=True)
df1 = df1.drop_duplicates(subset='Unique mail id').reset_index(drop=True)

#fix that pesky date issue that I didn't fix before:
#the "Date of pull" colum is a good substitution for "Date" when "Date" is missing:
df1['isDate'] = df1.Date.apply(lambda x: '/' in str(x))
df1.loc[df1['isDate']==False,'Date'] = df1.loc[df1['isDate']==False,'Date of pull']

#save a copy of transaction data with all files merged and Errors fixed
df1.to_csv(path.format("all_transactions.csv"),encoding="utf-8")

df2 = pd.read_csv(path.format("Home Data - Event Log.csv"),encoding="utf-8")
#need an dateString to index
#df2['Date'] = 'mm/dd/yyy'
df2['Date'] = df2['Month'].map(str) + "/" + df2['Day'].map(str) + "/" + df2['Year'].map(str)

#aggregating activities by day
activities = pd.DataFrame(df2.pivot_table(index="Date",columns="Activity",values="Duration",aggfunc="sum"))

#aggregating expenses by day
expenses = pd.DataFrame(df1.pivot_table(index="Date",columns="Category",values="Amount",aggfunc="sum"))


cor_sheet = pd.merge(activities,expenses,left_index=True,right_index=True,how="outer").corr()
#Save the merged data sheet:
pd.merge(activities,expenses,left_index=True,right_index=True,how="outer").to_csv(path.format("all_data.csv"),encoding="utf-8")
df = pd.merge(activities,expenses,left_index=True,right_index=True,how="outer")
df['Date'] = df.index

def fixYear(x):
	try:
		y = datetime.strptime(x, '%m/%d/%Y')
	except:
		y = datetime.strptime(x, '%m/%d/%y')
	return y
df['dataObje'] = df['Date'].apply(lambda X: fixYear(X))

df = df.sort('dataObje')	
small_df = df[df['dataObje']>datetime.strptime("11/15/2015", '%m/%d/%Y')]

writer = pd.ExcelWriter(path.format('output.xlsx'))
cor_sheet.to_excel(writer,'correlations')
activities.to_excel(writer,'activities')
expenses.to_excel(writer,'expenses')
writer.save()

