# Quantified-Self
Collection of files that I use to study my own behavior

##IFTTT Translator
This transforms IFTTT events into a dataframe that is more suited for data analysis. 
###IFTTT input format:
November 17, 2015 at 11:54AM	WorkWifi	Leaving Work\n
November 17, 2015 at 04:19PM	HomeWifi	Arriving at Home\n
November 17, 2015 at 06:19PM	HomeWifi	Leaving Home\n

###Google Sheets(output format):
Year	Month	Day	Hour	Duration	Activity\n
2015	11	17	11	265	Going from work to home\n
2015	11	17	16	120	Hanging out at home\n
2015	11	17	18	2	Went out, not to work\n
