import matplotlib 
matplotlib.use('ggplot')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from __future__ import print_function
from time import time
from collections import Counter

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

n_samples = 2000
n_features = 10000
n_topics = 10
n_top_words = 20
weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def get_single_topic(lda, tf_feature_names, n_top_words, topic):
	'''
	df1 = get_single_topic(lda, tf_feature_names, n_top_words, topic)
	'''
	words = [tf_feature_names[i] for i in lda.components_[topic].argsort()[:-n_top_words - 1:-1]]
	scores = lda.components_[topic][lda.components_[topic].argsort()[:-n_top_words - 1:-1]]
	df = pd.DataFrame(index=words,columns=['topic_{}'.format(topic)],data=scores)
	return df

def get_topic_names(lda, tf_feature_names, n_top_words, n_topics):
	themes = pd.Series()
	for topic in range(n_topics):
		theme = " ".join([tf_feature_names[i] for i in lda.components_[topic].argsort()[:-n_top_words - 1:-1]])
		themes.loc['topic_{}'.format(topic)] = theme
	return themes
		
def get_all_topics(lda, tf_feature_names, n_top_words,n_topics):
	'''
	df = get_all_topics(lda, tf_feature_names, n_top_words,n_topics)
	'''
	df = pd.DataFrame()
	for topic in range(n_topics):
		tmpdf = get_single_topic(lda, tf_feature_names, n_top_words, topic)
		for item in tmpdf.index:
			df.loc[item,'topic_{}'.format(topic)] = tmpdf.loc[item,'topic_{}'.format(topic)]
	return df

def get_day_of_week(x):
	try:
		y = datetime.strptime(x, '%m/%d/%Y')
	except:
		y = datetime.strptime(x, '%m/%d/%y')	
	return weekdays[y.weekday()]

def weekend_or_work_week(x):
	try:
		y = datetime.strptime(x, '%m/%d/%Y')
	except:
		y = datetime.strptime(x, '%m/%d/%y')	
	weekday = weekdays[y.weekday()]
	if weekday in ["Friday","Saturday"]:
		answer = "WeekendNight"
	else:
		answer = "WorkNight"
	return answer

def score_document(doc_dic,df,lda, tf_feature_names, n_top_words, n_topics,
					returnDF=True,confidence=.01):
	'''
	gives scores to the origional document, assigning a category to each one. 
	
	returnDF : By default returns a DataFrame, set to false to return a dict.
	confidence : this is the threashold that the model must meet to match the document to a topic.
	set to .01 to include practically everything, set to .99 to include almost nothing.
	
	
	document_scores = score_document(doc_dic,df,lda, tf_feature_names, n_top_words, n_topics)
	'''
	results_dict = {}
	for key in doc_dic.keys():
		document = doc_dic[key]
		words = [tf_feature_names[i] for i in tf.getrow(doc_dic.keys().index(key)).indices]
		scores = df[[word in words for word in df.index]]
		TM_Score = pd.DataFrame()
		TM_Score['docScore'] = scores.sum() 
		TM_Score['globalScore'] = df.sum()
		TM_Score['relevance'] = TM_Score['docScore']/TM_Score['globalScore']
		TM_Score['theme'] = get_topic_names(lda, tf_feature_names, n_top_words, n_topics)
		results = TM_Score['relevance'].fillna(0).to_dict()
		results['document'] = document
		results['top_score'] = TM_Score['relevance'].max()

		if TM_Score['relevance'].max() >= confidence:
			results['top_theme'] = TM_Score['theme'][TM_Score['relevance'].tolist().index(TM_Score['relevance'].max())]					
			results['top_topic'] = TM_Score.index[TM_Score['relevance'].tolist().index(TM_Score['relevance'].max())]
		else: 
			results['top_theme'] = 'unassigned'
			results['top_topic'] = 'unassigned'
		results_dict[key] = results
	if returnDF:
		return pd.DataFrame(results_dict).T
	else:
		return results_dict
		
		
#------------------------------------------------------------------------------------------	
###Begin - Here:  MODEL TRAINING
#------------------------------------------------------------------------------------------

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
			
doc_dic = {}
for i in np.unique(transactions['Date']):
	subset = transactions[transactions['dataObje']==i]
	reciept_list = [r for r in subset['Reciept text'].tolist() if r not in stop_list]
	cat_list = subset['Category'].dropna().tolist()
	tokens = []
	#list of all of the reciepts:
	for reciept in reciept_list:
		tokens.append("".join([x for x in reciept if x.lower() in "abcdefghijklmnopqrstuvwxyz1234567890"]))
	#list of all of the categories:
	for cat in cat_list:		
		tokens.append("".join([x for x in cat if x.lower() in "abcdefghijklmnopqrstuvwxyz1234567890"]))
	#add the day of the week as a feature:
	tokens.append(get_day_of_week(i))
	#add the weekend/weekday as a feature:
	#tokens.append(weekend_or_work_week(i)) #Turns out that weekend/workday just confused the model
	doc_dic[i] = " ".join(tokens)

data_samples = doc_dic.values()
	
# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
								stop_words='english')
								
tf = tf_vectorizer.fit_transform(data_samples)


# Fit the LDA model
print("Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                learning_method='online', learning_offset=50.,
                                random_state=0)
lda.fit(tf)
tf_feature_names = tf_vectorizer.get_feature_names()


#get output as a DataFrame
df = get_all_topics(lda, tf_feature_names, n_top_words,n_topics)

#------------------------------------------------------------------------------------------	
###SCORING INDIVIDUAL DOCUMENTS
#------------------------------------------------------------------------------------------


#DF that scores an individual document against each topic 
document_scores = score_document(doc_dic,df,lda, tf_feature_names, n_top_words, n_topics)
	
#to see the distribution of scores:
#this is usefull for understanding how good the model is at placing individual documents. 
document_scores['top_score'].hist(bins=60)

labels,values = zip(*Counter(document_scores['top_topic'].tolist()).items())

indexes = np.arange(len(labels))
width = 1
plt.bar(indexes, values, width)
plt.xticks(indexes + width * 0.5)
plt.show()

document_scores['top_score'].describe()
	