
# coding: utf-8

## Breaking down and studying my QS data

# Better living through data. One of my favorite hobbies is to use data to get a better understanding of my habits. Using both my IFTTT data and my Finance App

# In[1]:

#libraries that I'm using
import pandas as pd
import numpy as np
from datetime import datetime


### Getting the finance data:

# In[2]:

#path to my files (I'll come back here a lot so
#I'll keep this as a global variable)
path = "C:\Users\Bill\Google Drive\Finance\{}"


# In[3]:

#I keep my archived finance data in CSVs
finance_files = ["transactions2014.csv",
                "transactions2015_1.csv",
                "transactions2015_2.csv",
                "transactions2016.csv"]


# In[4]:

frames = [pd.read_csv(path.format(x)) for x in finance_files]
df = pd.concat(frames).reset_index(drop=True)
df = df.drop_duplicates(subset='Unique mail id').reset_index(drop=True)
df.head()


# After collecting data for most of 2014, I made some major changes in the application that affected the dates.  Really I wanted to just clean it out and forget it but I thought that this would be a good data cleaning example:

# In[5]:

#fix that pesky date issue that I didn't fix before:
df['isDate'] = df.Date.apply(lambda x: '/' in str(x))
df.loc[df['isDate']==False,'Date'] = df.loc[df['isDate']==False,'Date of pull']
df.head()


# OK cool but some of the data is '%m/%d/%Y' and some of it is '%m/%d/%y'.   OR 1/1/2014 and 1/1/14.  That's a problem. The fixYear function might not be the best but is fine for this as there are only two different scenarios.

# In[6]:

def fixYear(x):
	try:
		y = datetime.strptime(x, '%m/%d/%Y')
	except:
		y = datetime.strptime(x, '%m/%d/%y')
	return y
df['dataObje'] = df['Date'].apply(lambda X: fixYear(X))


# In[7]:

df['dataObje'][1]


# Awesome, I have a timestamp object for each transaction. This will come in handy later.

# IFTTT is collected and filtered in annother process (google app script). look in the IFTTT_event_translations.js. Here I'm loading that file from CSV.

### Adding the IFTTT data:

# In[8]:

df2 = pd.read_csv(path.format("Home Data - Event Log_2.csv"),encoding="utf-8")  #Log_2 because I made a backup.


# In[9]:

df2.head()


# Now I need a timestamp that matches the one from the finance data:

# In[10]:

df2['Date'] = df2['Month'].map(str) + "/" + df2['Day'].map(str) + "/" + df2['Year'].map(str)
df2.head()


### Transforming and merging the two sets together:

#### First the Activity data:

# In[11]:

activities = pd.DataFrame(df2.pivot_table(index="Date",columns="Activity",values="Duration",aggfunc="sum"))
#I'm only showing a subset of the columns to the public
cols =  ["Going from home to work",
		"Going from work to home",
		"Hanging out at home",
		"Left work for a bit, and came back",
		"Went out, not to work",
		"Working"]
activities = activities[cols]
activities.head()


#### Then the expense data:

# In[12]:

expenses = pd.DataFrame(df.pivot_table(index="Date",columns="Category",values="Amount",aggfunc="sum"))
#I'm only showing a subset of the columns to the public
cols =  ['Arts&Crafts', 
		'Coffee', 
		'Eating at Home', 
		'Eating out', 
		'Grocery', 
		'Lunch', 
		'Out for drinks',
		'Out of town',  
		'Transportation']
expenses = expenses[cols]
expenses.head()


#### Then you merge:

# Note: My IFTTT data only goes back to November 2015. So lots of blanks.

# In[13]:

data = pd.merge(activities,expenses,left_index=True,right_index=True,how="outer")
data.head()


# Check to see if that matched right

# In[14]:

print (activities['Hanging out at home']['1/1/2016']/60, activities['Went out, not to work']['1/1/2016']/60)


# Yup. New Year’s day I was at home pretty much the whole day. It's over 24 hours because it counts the number of minutes until the next log event (aka leaving home). In that case there could be more than 24 hours of an activity. The best way to think about it is that 1/1/2016 is the day that a 28 hour activity began. Also went out for about 3.5 hours that day and bought some groceries, so cool.

#### Output to Excel for manual analysis:

# In[15]:

writer = pd.ExcelWriter(path.format('output.xlsx'))
data.to_excel(writer,'all data')
data.corr().to_excel(writer,'correlation')
activities.to_excel(writer,'activities')
expenses.to_excel(writer,'expenses')
df.to_excel(writer,'transactions')
df2.to_excel(writer,'IFTTT events')
writer.save()


# In[ ]:

data.corr()


# That's it. I'll write up another example of how to get findings in another Notebook. Data cleaning is a big part of the work and I wanted to get that portion separately.
