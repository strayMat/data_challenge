
# coding: utf-8

# In[2]:

import pandas as pd
import numpy as np
from Calculhoraire import intervalle
from datetime import datetime

print("loading data...")
df = pd.read_csv("train_2011_2012_2013.csv", sep = ";", usecols = list(["DATE","ASS_ASSIGNMENT"]))
print("end! ")


# In[3]:

print(df.head())
print(len(df))


# In[4]:


#création de colonne TIME_SLOT et DAY_WE_DS, conversion des jours de la semaine en numéro
print("Convert date format...")
df['TIME_SLOT'] = df['DATE'].apply(lambda x:     intervalle(x))
df["DATE"] = df["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
df['DAY_WE_DS'] = df['DATE'].dt.weekday
print("end conversion")


# In[6]:

#nombre de jours qu'on regarde 
nb_days = len(np.unique(df['DATE'].dt.date))
#nombre de semaines (144 normalement)
nb_semaines = nb_days/7
print(nb_semaines)

ass = np.unique(df.ASS_ASSIGNMENT)
print(ass)


# In[7]:

#creation du dataframe de stats:
dstat = pd.DataFrame({'count' : df.groupby(['ASS_ASSIGNMENT', 'DAY_WE_DS','TIME_SLOT']).size()}).reset_index()
dstat["MEAN"] = dstat["count"]/nb_semaines
print(dstat.head())


# In[8]:

dsub = pd.read_csv('submission.txt', sep = "\t")

print(dsub.head())

#on modifie l'entree afin de pouvoir recuperer les infos de statistiques
entree = dsub
entree['TIME_SLOT'] = entree['DATE'].apply(lambda x: intervalle(x))
entree["DATE"] = entree["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
entree['DAY_WE_DS'] = entree['DATE'].dt.weekday

print(entree.head())


# In[9]:

prediction = []
for row in entree.iterrows():
    ass = row[1]['ASS_ASSIGNMENT']
    time = row[1]['TIME_SLOT']
    wk = row[1]['DAY_WE_DS']
    pred = dstat[(dstat['TIME_SLOT']== time) & (dstat['DAY_WE_DS']== wk) & (dstat['ASS_ASSIGNMENT']==ass)]['MEAN'].values[0]
    prediction.append(pred)
    if (row[0]%5000 ==0):
        print(row[0])


# In[18]:

#conversion en entiers
prediction1 = [int(round(x)) for x in prediction]
for i in range(len(prediction1)):
    if ((prediction1[i] >100) & (prediction1[i]<200)):
        prediction1[i] = 0
    if prediction1[i] == 0:
        prediction1[i] = 1 
print(prediction1)


# In[19]:

dsub = pd.read_csv('submission.txt', sep = "\t")
dsub['prediction'] = prediction1
print(dsub.head())


# In[20]:

dsub.to_csv("sortie.txt", sep = '\t', index = False)


# In[ ]:



