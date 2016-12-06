
# coding: utf-8

# In[28]:

from datetime import datetime
import pandas as pd
from Calculhoraire_exclusif import intervalle
from Calculhoraire_exclusif import centre
from Calculhoraire_exclusif import holidays
from Calculhoraire_exclusif import inverse
from sklearn.tree import DecisionTreeRegressor
from sklearn import ensemble
import numpy as np
from math import ceil

read_name = 'train_week_centre_time_date.csv'
print("loading data...")
df = pd.read_csv(read_name, sep = ",")
print("end loading\n")

df['WEEK_END']=df['DAY_WE_DS'].apply(lambda x:     int(x>=5))

print(df.head())
print(len(df))

#limits for each assignment
#limits=[300,1,1,70,0,3,70,0,12,5,4,7,0,12,5,10,55,80,2,14,70,25,15,100,425,120,120,1400]
limits = [0 for i in range(28)]
for i in range(28):
    limits[i]=df[(df.ASS_ASSIGNMENT==i) & ((df.YEAR>2012) | ((df.YEAR==2012) & (df.MONTH>=6)))].CSPL_RECEIVED_CALLS.max(axis=0)
    
print(limits)

n_iterations=[0 for i in range(28)]
for i in range(28):
    if limits[i]>=80:
        n_iterations[i]=1000
    elif limits[i]>=40:
        n_iterations[i]=500
    elif limits[i]>=20:
        n_iterations[i]=200
    else:
        n_iterations[i]=70
print(len(limits))
print(len(n_iterations))

assign = np.unique(df.ASS_ASSIGNMENT)
print(assign)

clf = []
for i in assign:
    clf.append(ensemble.GradientBoostingRegressor(loss='ls', n_estimators=n_iterations[i], verbose=1, presort='auto'))

for i in assign:
    Matrix = df[df["ASS_ASSIGNMENT"]==i]
    Matrix = Matrix[['YEAR','MONTH','DAY','TIME_SLOT','HO','DAY_WE_DS','WEEK_END']]
    Result = df[df['ASS_ASSIGNMENT']==i]
    #Result['CSPL_RECEIVED_CALLS'] = Result['CSPL_RECEIVED_CALLS'].apply(lambda x: exp(x))
    Result = Result['CSPL_RECEIVED_CALLS']
    print(inverse(i))
    clf[i].fit(Matrix, Result)


# In[13]:

dsub = pd.read_csv('submission.txt', sep = "\t")
print(dsub.head())
print("convert to timestamp...")
dsub["DATE"] = dsub["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
dsub["short_DATE"] = dsub["DATE"].apply(lambda x:     datetime.strftime(x,"%Y-%m-%d"))
dsub['HO'] = dsub['short_DATE'].apply(lambda x: holidays(x))
print("End of conversion!")


dsub['DAY_WE_DS'] = dsub['DATE'].dt.weekday
dsub['WEEK_END'] = dsub['DAY_WE_DS'].apply(lambda x:     int(x>=5))
dsub['DAY'] = dsub['DATE'].dt.day
dsub['MONTH'] = dsub['DATE'].dt.month
dsub['YEAR'] = dsub['DATE'].dt.year
dsub['TIME_SLOT'] =dsub['DATE'].apply(lambda x: intervalle(x))


# In[16]:

prediction = []
for row in dsub.iterrows():
    ass = row[1]['ASS_ASSIGNMENT']
    if limits[centre(ass)] == 0:
        prediction.append(0)
        continue
    time = row[1]['TIME_SLOT']
    wk = row[1]['WEEK_END']
    dayds = row[1]['DAY_WE_DS']
    month = row[1]['MONTH']
    year = row[1]['YEAR']
    day = row[1]['DAY']
    holidays = row[1]['HO']
    pred = clf[centre(ass)].predict([[year,month,day,time,holidays,dayds,wk]])
    pred = max(0,pred)
    pred = min(limits[centre(ass)]/2,pred)
    pred = 2*pred
    prediction.append(pred)

#arrondit à l'entier le plus proche
prediction = [int(x) for x in prediction]

#mise à jour
dsub['prediction']=prediction
dsub['DATE']=dsub['DATE'].apply(lambda x:     datetime.strftime(x,"%Y-%m-%d %H:%M:%S"))
dsub['DATE']=dsub['DATE']+'.000'
header = ['DATE', 'ASS_ASSIGNMENT', 'prediction']
#Ecriture
dsub.to_csv("sortie.txt", columns = header, sep = '\t', index = False)


# In[ ]:



