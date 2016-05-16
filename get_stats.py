###
#KEY VARIABLES
pc = 2 # The percent change to report on
days = 30 # How many days to retrieve on each pull
volume = 1 # Daily = 1, Weekly = 7, Monthly = 30
report_type = 'new' #can be 'active' or 'new'
group_by = "country"   #Grouping can be 'country' for country, for other possible groupings, check Amplitude docs.
km = ['Australia','Canada','France','Germany','Italy','Spain','United Kingdom','United States'] #Define the key markets that are the most important to you.
###


##Enter your secret Amplitude keys here (or better yet, use a python library like keylib to obscure them from your script)
android_api_key = "123"
android_secret_key = "123"
ios_api_key = "123"
ios_secret_key = "123"


#Import needed libraries
import pandas as pd
import numpy as np
import time
import datetime
import requests as re
from requests.auth import HTTPBasicAuth
import matplotlib.pyplot as plt


#Get today's date
today = datetime.date.today() - datetime.timedelta(days=1)
yesterday = datetime.date.today() - datetime.timedelta(days=2)
last_week = datetime.date.today() - datetime.timedelta(days=8)
date_limit = datetime.date.today() - datetime.timedelta(days=days+1)

#Put the date in string format for constructing the URL
url_date = today.strftime('%Y%m%d')
url_date_limit = date_limit.strftime('%Y%m%d')

#Function for making a call to the Amplitude API and returning the appropriate data
def getAmplitudeData(reportType, grouping, api_key, secret_key):
        #Build the request URL
        url = "https://amplitude.com/api/2/users?m=" + reportType + "&start=" + url_date_limit + "&end=" + url_date + "&i=" + str(volume) + "&g=" + grouping

        #Make the GET request; returns response as JSON
        r = re.get(url, auth=HTTPBasicAuth(api_key, secret_key))

        df = pd.DataFrame(r.json())

        values = df.iloc[0,0]
        index = df.iloc[1,0]
        dates = df.iloc[3,0]

        df = pd.DataFrame(values, index=index, columns=dates)
        data = pd.DataFrame(values, index=index, columns=dates)

        x = len(df.columns)
        today_col = df.columns[x-2]
        previous_col = df.columns[x-3]


        #Create new column which is the standard deviation of all columns in that row
        df['stdev'] = df.std(axis=1)
        df['change'] = (df[today_col] / df[previous_col] - 1)

        x = len(df.columns)

        #Print 
        print ("*** THESE CHANNELS INCREASED by more than " + str(pc) + "%")
        print (df.loc[df['change'] > pc, today_col])
        print ('\n\n')

        print ("*** THESE CHANNELS DECREASED by more than " + str(pc) + "%")
        print (df.loc[df['change'] < (-pc), today_col])
        print ('\n\n')
        
        if grouping == 'country':
                print (df.loc[km, 'change'])
                print ('\n\n')
                km_chart = data.loc[km]
                km_chart.T.plot()
        
        return df

#Call the getAmplitude() function for Android then iOS
df_and = getAmplitudeData(reportType=report_type, grouping = group_by, api_key=android_api_key, secret_key=android_secret_key)
df_ios = getAmplitudeData(reportType=report_type, grouping = group_by, api_key=ios_api_key, secret_key=ios_secret_key)

#Show plots
#plt.show()

