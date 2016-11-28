
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd


data_name = "train_2011_2012_2013.csv"
#toutes les colonnes
cols = ['DATE', 'ASS_ASSIGNMENT']

print("loading data...")
#attention retirer nrows pour sortir le fichier complet (moi ça fait bugger jupyter et je dois eteindre mon PC)
df = pd.read_csv(data_name, usecols = cols, sep = ";")
print("end loading\n")


# In[2]:

from Calculhoraire import intervalle
from Calculhoraire import centre
df['TIME_SLOT']=df['DATE'].apply(lambda x:     intervalle(x))
df['ASS_ASSIGNMENT']=df['ASS_ASSIGNMENT'].apply(lambda x:     centre(x))
from datetime import datetime
df['DATE'] = df['DATE'].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
df['DAY_WE_DS'] = df['DATE'].dt.weekday
df['short_DATE'] = df['DATE'].dt.date


# In[3]:

df2 = df.groupby(['short_DATE','DAY_WE_DS','ASS_ASSIGNMENT','TIME_SLOT']).size()


# In[4]:

levels = df2.index.levels[:2] + [list(range(18)), list(range(48))]
mult = 18 * 48
labels = [
    [], [], [i for i in range(18) for j in range(48)], [j for i in range(18) for j in range(48)] ]
li = None
n = 0
for i in zip(*df2.index.labels[:2]):
    if i!=li:
        n+=1
        li = i
        labels[0] += [i[0]] * mult
        labels[1] += [i[1]] * mult
labels[2] = labels[2] * n
labels[3] = labels[3] * n
names = df2.index.names
ind3 = pd.MultiIndex(levels=levels, labels=labels, names=names)
df3 = df2.reindex(ind3, fill_value=0)


# In[5]:

write_name = "testseries.csv"

df3.to_csv(write_name,header=True)


# In[6]:

read_name = 'AlmightyData.csv'
print("loading data...")
df = pd.read_csv(read_name, usecols = ['DAY_WE_DS','ASS_ASSIGNMENT','TIME_SLOT','N_Call'], sep = ",")
print("end loading\n")


# In[7]:

Matrix = df[['DAY_WE_DS','TIME_SLOT','ASS_ASSIGNMENT']]
Result = df[['N_Call']]


# In[8]:

from sklearn import tree
clf = tree.DecisionTreeRegressor()
clf = clf.fit(Matrix, Result)


# In[9]:

print(clf.predict([[5,0,0]]))


# In[17]:

dsub = pd.read_csv('submission_tab.txt', sep = "\t")


# In[18]:

print(dsub.head())


# In[19]:

from Calculhoraire import inter

dsub['TIME_SLOT'] =dsub['HOUR'].apply(lambda x:     inter(x))
dsub['DATE'] = dsub['DATE'].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d"))
dsub['DAY_WE_DS'] = dsub['DATE'].dt.weekday


# In[20]:

prediction = []
for row in dsub.iterrows():
    ass = row[1]['ASS_ASSIGNMENT']
    time = row[1]['TIME_SLOT']
    wk = row[1]['DAY_WE_DS']
    pred = clf.predict([[centre(ass),wk,time]])
    prediction.append(pred)


# In[21]:

from math import round
prediction = [round(x) for x in prediction]


# In[22]:

dsub['prediction']=prediction

print(dsub.head())


# In[23]:

dsub.to_csv("sortie.csv", sep = ',', index = False)


# In[27]:

dsubFirst = pd.read_csv('sortie.csv')

print(dsubFirst.head())


# In[31]:

dsubFirst.to_csv('sortie1.txt', sep = '\t', index = False)


# In[ ]:



