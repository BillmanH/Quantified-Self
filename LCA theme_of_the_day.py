'''
dividing my recipts into themes usin Gensim
-using the time-series dictionary (doc_dic) from analysis.py 
-and all of the libraries and globals in that file.
'''
import gensim as g
import nltk



#------------------ CLEANING -----------------------------
df = df1.copy() #backup just in case I mess it up :)

doc_dic
#the documents don't actually get into the data file
documents = df['Reciept text'].values.tolist()

#------------------ LEXILIZING -----------------------------
#this extra step removes all words that aren't nouns verbs or adjectives
def nouns_verbs_and_adjectives_only(document):
	text = nltk.word_tokenize(document)
	tags = nltk.pos_tag(text)
	new_list = [x[0] for x in tags if x[1] in words_we_like]
	return cut_chars(' '.join(new_list))
documents = [nouns_verbs_and_adjectives_only(document) for document in documents]
	
stoplist = nltk.corpus.stopwords.words()
texts = [[item for item in document]
	for document in documents]
	
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
	for token in text:
		frequency[token] += 1
		
texts = [[token for token in text if frequency[token] > 1]
	for text in texts]
	
dictionary = g.corpora.Dictionary(texts)

#!!!! save here so that you don't have to go back a million times. 
dictionary.save(work_directory.format("dictionary.dict")) # store the dictionary, for future reference

corpus = [dictionary.doc2bow(text) for text in texts]

#------------------ MODELING -----------------------------

n_topics = 10
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

#adding the scores to the corpus
for row in range(len(df)):
	doc_bow = dictionary.doc2bow(texts[row])
	for x in model[doc_bow]:
		df.loc[row,"topic_{}".format(str(x[0]))] = x[1]


#to look at the top words (quick glimpse)
nw = 20  #number of words that you want to show
sortby = 40 #topic that you want to sort by
topicsList = [40,41,64] #list of topic numbers that you want to see.
topicsList = map(str,topicsList)
top_words.sort(columns=[str(sortby)], ascending=False).ix[:nw,topicsList]


#------------------ GRAPHING -----------------------------

#------------------ OUTPUTS -----------------------------

#limit the size of the full text to a tweet
df['fullText'] = df['fullText'].str[:250]
#or drop full text entirely
df = df.drop('fullText',axis=1)

#out to excel:
writer = pd.ExcelWriter(work_directory.format('SW_dataset.xlsx'),engine ='xlsx')
top_words.to_excel(writer,'word list',encoding='utf-8')
df.to_excel(writer,'data frame',encoding='utf-8')
writer.save()

#or to individual CSV sheets: because I can't figure the excel thing out right now.
top_words.to_csv(work_directory.format('topWords.csv'),encoding='utf-8')
df.to_csv(work_directory.format('all_mentions.csv'),encoding='utf-8')