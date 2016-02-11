# Quantified-Self
Collection of files that I use to study my own behavior

##IFTTT Translator
This transforms IFTTT events into a dataframe that is more suited for data analysis. 
###IFTTT input format:
IFTT date | Connection Trigger | Text from Recipe
------------ | -------------| -------------
November 17, 2015 at 11:54AM |	WorkWifi |	Leaving Work
November 17, 2015 at 04:19PM |	HomeWifi |	Arriving at Home
November 17, 2015 at 06:19PM |	HomeWifi |	Leaving Home


###Google Sheets(output format):
Year |	Month |	Day |	Hour |	Duration |	Activity
-----|------- | -----|--------| ------|-------
2015 |	11 |	17 |	11 |	265 |	Going from work to home
2015 |	11 |	17 |	16 |	120 |	Hanging out at home
2015 |	11 |	17 |	18 |	2 |	Went out, not to work

Duration is in minutes.


##Transformation and Vizualisation
I've placed all of the data transformation and basic analysis into a couple of ipython notebooks in order 
to make it easier to study the process and outcome.
### Gathering and Cleaning the data:
<a href="https://github.com/BillmanH/Quantified-Self/blob/master/Joining%20and%20cleaning%20data.ipynb">Joining and cleaning data.ipynb</a>
### Running statistics and making charts:
<a href="https://github.com/BillmanH/Quantified-Self/blob/master/QS_analysis.ipynb">QS_analysis.ipynb</a>
### Model to try and guess what I am doing at any moment:
<a href="https://github.com/BillmanH/Quantified-Self/blob/master/what%20am%20I%20doing%20right%20now.ipynb">QS_analysis.ipynb</a>