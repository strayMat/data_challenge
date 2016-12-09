
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
from datetime import datetime
from Calculhoraire_exclusif import holidays
from Calculhoraire_exclusif import centre
from Calculhoraire_exclusif import intervalle

#Having weeks to be predicted
predict_intervals = pd.read_csv('predict_weeks/intervals.csv', sep=';')

predict_intervals = predict_intervals.as_matrix()

data_name = "train/train_2011_2012_2013.csv"
cols = ['DATE', 'ASS_ASSIGNMENT', 'CSPL_RECEIVED_CALLS']

print("loading data...")
df = pd.read_csv(data_name, usecols = cols, sep = ";")
print("end loading\n")

start = '2011-01-01 00:00:00.000'
start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")

df['TIME_SLOT']=df['DATE'].apply(lambda x:     intervalle(x))
df['ASS_ASSIGNMENT']=df['ASS_ASSIGNMENT'].apply(lambda x:     centre(x))
df['DATE'] = df['DATE'].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
df['DAY_WE_DS'] = df['DATE'].dt.weekday
df['short_DATE'] = df['DATE'].dt.date
#Splitting the data in subsets
#1800s in a 30min slot
df["ABSOLUTE"] = df['DATE'].apply(lambda x:     ((x-start).days)*48)

df['short_DATE'] = df['short_DATE'].apply(lambda x:     datetime.strftime(x,"%Y-%m-%d"))
df['HO']=df['short_DATE'].apply(lambda x:     holidays(str(x)))
df["MONTH"] = df['short_DATE'].apply(lambda x: int(x.split("-")[1]))
df["YEAR"] = df['short_DATE'].apply(lambda x: int(x.split("-")[0]))
df["DAY"] = df['short_DATE'].apply(lambda x: int(x.split("-")[2]))

df2 = df.groupby(['short_DATE','YEAR','MONTH','DAY','DAY_WE_DS','TIME_SLOT','ABSOLUTE','HO','ASS_ASSIGNMENT'])['CSPL_RECEIVED_CALLS'].sum()


#splitting data for avoiding future
for i in range(12):
    df3 = df2[df2['ABSOLUTE']<predict_intervals[i][0]]
    write_name = "train/"+str(i)+"/train_week_centre_time_date.csv"
    df3.to_csv(write_name,header=True)

