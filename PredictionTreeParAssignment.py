
# coding: utf-8

# In[ ]:

from datetime import datetime
import pandas as pd
from Calculhoraire_exclusif import intervalle
from Calculhoraire_exclusif import centre
from Calculhoraire_exclusif import holidays
from sklearn.tree import DecisionTreeRegressor
from sklearn import ensemble
import numpy as np
from math import exp
from math import log
from math import ceil


read_name = 'train_week_centre_time_date.csv'
print("loading data...")
df = pd.read_csv(read_name, sep = ",")
print("end loading\n")


# In[108]:

df["MONTH"] = df['short_DATE'].apply(lambda x: int(x.split("-")[1]))
df["YEAR"] = df['short_DATE'].apply(lambda x: int(x.split("-")[0]))
df["DAY"] = df['short_DATE'].apply(lambda x: int(x.split("-")[2]))
df["HO"] = df['short_DATE'].apply(lambda x: holidays(x))
print(df.head())
print(len(df))


# In[109]:

assign = np.unique(df.ASS_ASSIGNMENT)
print(assign)


# In[111]:

clf = []
for i in assign:
    #clf.append(DecisionTreeRegressor())
    clf.append(ensemble.GradientBoostingRegressor(loss='quantile', learning_rate=0.1, n_estimators=500, subsample=1.0, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_depth=3, init=None, random_state=None, max_features=None, alpha=0.96, verbose=0, max_leaf_nodes=None, warm_start=False, presort='auto'))
for i in assign:
    Matrix = df[df["ASS_ASSIGNMENT"]==i]
    Matrix = Matrix[['DAY_WE_DS','TIME_SLOT','MONTH','YEAR','DAY','HO']]
    Result = df[df['ASS_ASSIGNMENT']==i]
    #Result['CSPL_RECEIVED_CALLS'] = Result['CSPL_RECEIVED_CALLS'].apply(lambda x: exp(x))
    Result = Result['CSPL_RECEIVED_CALLS']
    clf[i].fit(Matrix, Result)


# In[ ]:

dsub = pd.read_csv('submission.txt', sep = "\t")
print(dsub.head())
print("convert to timestamp...")
dsub["DATE"] = dsub["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
print("End of conversion!")


dsub['DAY_WE_DS'] = dsub['DATE'].dt.weekday
dsub['DAY'] = dsub['DATE'].dt.day
dsub['MONTH'] = dsub['DATE'].dt.month
dsub['HO'] = dsub['DATE'].apply(lambda x: holidays(x))
dsub['YEAR'] = dsub['DATE'].dt.year
dsub['TIME_SLOT'] =dsub['DATE'].apply(lambda x: intervalle(x))


# In[ ]:

prediction = []
for row in dsub.iterrows():
    ass = row[1]['ASS_ASSIGNMENT']
    time = row[1]['TIME_SLOT']
    wk = row[1]['DAY_WE_DS']
    month = row[1]['MONTH']
    year = row[1]['YEAR']
    day = row[1]['DAY']
    holidays = row[1]['HO']
    pred = clf[centre(ass)].predict([[wk,time,month,year,day,holidays]])
    prediction.append(max(0,pred))

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



