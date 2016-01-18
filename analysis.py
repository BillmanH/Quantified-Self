# processing the data in the output.xls file
import numpy as np
import pandas as pd
import math

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

expenses['Date'] = expenses.index
expenses['dataObje'] = expenses['Date'].apply(lambda X: fixYear(X))
expenses = expenses.sort('dataObje')	

#date time 

#counting the number of drinks per day
mergedDF['hadDrinks'] = mergedDF['Out for drinks']>0
drinksdf = mergedDF['numDrinks'] = mergedDF['Out for drinks'].apply(lambda x: math.ceil(x/10)).dropna()
days_drinks = mergedDF['numDrinks'] = mergedDF['Out for drinks'].apply(lambda x: math.ceil(x/10)).fillna(0)
days_drinks.resample('W',how='sum')

singleVarHistogram(np.array(days_drinks.tolist()),bins=30,title="Distribution of drinks",xaxis="#")
days_drinks.describe()
drinksByWeek = pd.DataFrame(days_drinks.resample('W',how='sum'))
drinksByWeek['limit'] = 15
drinksByWeek['control'] = drinksByWeek['Out for drinks'] - drinksByWeek['limit']
drinksByWeek['over'] = drinksByWeek['control'] > 0

bunchOfVarLine([np.array(drinksByWeek['Out for drinks']),
				np.array(drinksByWeek['limit'])],
				['drinks','limit'],
				label="chart")


plt.plot(x_pos,np.array(drinksByWeek['control']),
		label='level of control',
		color=tahzoo_colors[1])
		
plt.bar(x_pos,np.array(drinksByWeek['control']),
		label='level of control',
		color=tahzoo_colors[1])

len(drinksByWeek[drinksByWeek['over']])/float(len(len(drinksByWeek)))
				
#getting a bag of words model. 
import gensim as g
import nltk

df1['dataObje'] = df1['Date'].apply(lambda X: fixYear(X))

doc_dic = {}
for i in np.unique(df1['dataObje']):
	subset = df1[df1['dataObje']==i]
	doc_dic[i] = subset['Reciept text'].tolist()
	
documents = doc_dic.values()
docKeys = doc_dic.keys()

stop_list = ["SOYLENT",
			"BROWNPAPERTICKETS...",
			"ADDRESS CHANGE",
			"AMTRAK CASCADES Q12",
			"VIRGINIA MASON FR...",
			"UDACITY&nbsp; INC",
			"VENDINI TICKETS",
			"Metrix Communicat...",
			"TICKETWEB",
			"BOLTBUS - INTERNE...",
			"Amazon web services",
			"Amazon Web Services",
			"AMTRAK",
			"UDEMY.COM",
			"NETFLIX.COM",
			"DSC",
			"ALASKA AIRLINE AS...",
			"Kappes Miller Man...",
			"SOUND TRANSIT - S..."]
			
texts = [[item for item in document if item not in stop_list]
	for document in documents]
	
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
	for token in text:
		frequency[token] += 1
		
texts = [[token for token in text if frequency[token] > 1]
	for text in texts]

dictionary = g.corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]


n_topics = 20
model = g.models.ldamodel.LdaModel(corpus,
										id2word=dictionary,
										num_topics=n_topics,
										passes=4) #increasing the passes increases time.

										
										
#------------------ ********* -----------------------------
#------------------ REPORTING -----------------------------
#------------------ ********* -----------------------------
results = model.print_topics(num_topics=n_topics, num_words=50)

results_matrix = [[[b for b in a.split("*")] for a in result.split(" + ")] for result in results]

#getting the top words lists (limit is .0000)
top_words = pd.DataFrame()
for index,item in enumerate(results_matrix):
	for word in item:
		top_words.loc[word[1],str(index)] = float(word[0])			

scored_docs = pd.DataFrame()
#adding the scores to the corpus
for item in doc_dic.items():
	doc_bow = dictionary.doc2bow(item[1])
	for x in model[doc_bow]:
		scored_docs.loc[item[0],"topic_{}".format(str(x[0]))] = x[1]	
	
#out to excel:
writer = pd.ExcelWriter(path.format('reciept_model.xlsx'))
top_words.to_excel(writer,'word list',encoding='utf-8')
scored_docs.to_excel(writer,'data frame',encoding='utf-8')
writer.save()

%save C:\\Users\\Bill\\Desktop\\Fun Stuff\\my_QA_session 1-103

