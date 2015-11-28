# Quantified-Self
Collection of files that I use to study my own behavior

##IFTTT Translator
This transforms IFTTT events into a dataframe that is more suited for data analysis. 
###IFTTT input format:
November 17, 2015 at 11:54AM	WorkWifi	Leaving Work
November 17, 2015 at 04:19PM	HomeWifi	Arriving at Home
November 17, 2015 at 06:19PM	HomeWifi	Leaving Home

###Google Sheets(output format):
Year	Month	Day	Hour	Duration	Activity
2015	11	17	11	265	Going from work to home
2015	11	17	16	120	Hanging out at home
2015	11	17	18	2	Went out, not to work
