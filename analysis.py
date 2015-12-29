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
activities['Date'] = activities['Date'].str.replace(r"/14$","/2014")
activities['Date'] = activities['Date'].str.replace(r"/2016$","/2015")
activities.index = pd.to_datetime(pd.Series(activities['Date']))


pd.merge(activities,expenses,left_index=True,right_index=True,how="outer")
