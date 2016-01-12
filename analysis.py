# processing the data in the output.xls file
import numpy as np
import pandas as pd

path = "C:\Users\Bill\Desktop\Fun Stuff\{}"

activities =  pd.read_excel(path.format("output.xlsx"),
							sheetname="activities",
							skiprows=[1])

expenses =  pd.read_excel(path.format("output.xlsx"),
							sheetname="expenses",
							skiprows=[1])
							
#found some errors in the Dates:
#/14 needs to be /2014
expenses['Date'] = expenses.index
expenses['Date'] = expenses['Date'].str.replace(r"/14$","/2014")
expenses.index = pd.to_datetime(pd.Series(expenses['Date']))

#2016 is an error in the IFTTT script, I think
activities['Date'] = activities.index
activities['Date'] = activities['Date'].str.replace(r"/2016$","/2015")
activities.index = pd.to_datetime(pd.Series(activities['Date']))


mergedDF = pd.merge(activities,expenses,left_index=True,right_index=True,how="outer")

def fixYear(x):
	try:
		y = datetime.strptime(x, '%m/%d/%Y')
	except:
		y = datetime.strptime(x, '%m/%d/%y')
	return y
mergedDF['dataObje'] = mergedDF['Date'].apply(lambda X: fixYear(X))
mergedDF['Date'] = mergedDF.index
#checking the 2016 year issue:
Data_2016 = mergedDF[mergedDF['dataObje']>datetime.strptime("1/1/2016", '%m/%d/%Y')]

#now I'm going to export to excel because I can eplore better there. 
mergedDF.to_csv(path.format("mergedDF.csv"),encoding="utf-8")
mysubset = ['Going from work to home','Out for drinks']


def getX_Y(df,mysubset):
	'''x,y = getX_Y(mergedDF,mysubset)'''
	subset = df.dropna(0,subset=mysubset)[mysubset]
	x = subset[mysubset].loc[:,mysubset[0]].tolist()
	y = subset[mysubset].loc[:,mysubset[1]].tolist()
	return np.asarray(x),np.asarray(y)
	
def getX(df,col):
	'''x,y = getX_Y(df,col)'''
	subset = df.dropna(0,subset=[col])
	x = subset[col].tolist()
	return np.asarray(x)

mysubset = ['Going from work to home','Out for drinks']
x,y = getX_Y(mergedDF,mysubset)
compareTwoArrays(x,y,kind='reg')

mysubset = ['Grocery','Out for drinks']
x,y = getX_Y(mergedDF,mysubset)
compareTwoArrays(x,y,kind='reg')

#dividing by quarter:
dfQ1 = mergedDF[(mergedDF['dataObje']>datetime.strptime("1/1/2015", '%m/%d/%Y'))&(mergedDF['dataObje']<datetime.strptime("3/31/2015", '%m/%d/%Y'))]
dfQ2 = mergedDF[(mergedDF['dataObje']>datetime.strptime("4/1/2015", '%m/%d/%Y'))&(mergedDF['dataObje']<datetime.strptime("6/30/2015", '%m/%d/%Y'))]
dfQ3 = mergedDF[(mergedDF['dataObje']>datetime.strptime("7/1/2015", '%m/%d/%Y'))&(mergedDF['dataObje']<datetime.strptime("9/30/2015", '%m/%d/%Y'))]
dfQ4 = mergedDF[(mergedDF['dataObje']>datetime.strptime("10/1/2015", '%m/%d/%Y'))&(mergedDF['dataObje']<datetime.strptime("12/31/2015", '%m/%d/%Y'))]
singleVarHistogram(getX(dfQ1,'Out for drinks'),bins=15,title="Q1",xaxis="$")
singleVarHistogram(getX(dfQ2,'Out for drinks'),bins=15,title="Q2",xaxis="$")
singleVarHistogram(getX(dfQ1,'Out for drinks'),bins=15,title="Q3",xaxis="$")
singleVarHistogram(getX(dfQ2,'Out for drinks'),bins=15,title="Q4",xaxis="$")
singleVarHistogram(getX(mergedDF,'Out for drinks'),bins=25,title="Out for drinks",xaxis="$")
singleVarHistogram(getX(mergedDF,'Grocery'),bins=25,title="Out for drinks",xaxis="$")

myCols =  [u'Going from home to work', u'Going from work to home',
 u'Hanging out at home',  u'Left work for a bit, and came back', u'Went out, not to work',
 u'Working', u'Coffee', u'Eating at Home', u'Eating out', u'Grocery', u'Lunch',
 u'Out for drinks', u'Transportation']
 
df.gmail
 
#smaller dataset for just the days where I have activity data.
small_df = df[df['dataObje']>datetime.strptime("11/15/2015", '%m/%d/%Y')]
small_df[myCols].corr()
small_df[myCols].corr().to_csv(path.format("cor_sheet.csv"),encoding="utf-8")


expenses

expenses['Date'] = expenses.index
expenses['dataObje'] = expenses['Date'].apply(lambda X: fixYear(X))
expenses = expenses.sort('dataObje')	


#getting a bag of words model. 
df1['dataObje'] = df1['Date'].apply(lambda X: fixYear(X))
	
doc_dic = {}
for i in np.unique(df1['dataObje']):
	subset = df1[df1['dataObje']==i]
	doc_dic[i] = subset['Reciept text'].tolist()
	




