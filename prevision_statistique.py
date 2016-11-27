
# coding: utf-8

# In[25]:

import pandas as pd
import numpy as np
from Calculhoraire import intervalle
from datetime import datetime

dsub = pd.read_csv('submission.txt', sep = "\t")
dstat = pd.read_csv('statistiques.csv', sep = "," )
dstat = dstat.drop('Unnamed: 0', axis = 1)
print(dstat.head())
print(dsub.head())


# In[26]:

#on modifie l'entree afin de pouvoir recuperer les infos de statistiques
entree = dsub
entree['TIME_SLOT'] = entree['DATE'].apply(lambda x: intervalle(x))
entree["DATE"] = entree["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
entree['DAY_WE_DS'] = entree['DATE'].dt.weekday

print(entree.head())


# In[101]:

prediction = []
for row in entree.iterrows():
    ass = row[1]['ASS_ASSIGNMENT']
    time = row[1]['TIME_SLOT']
    wk = row[1]['DAY_WE_DS']
    pred = dstat[(dstat['TIME_SLOT']== time) & (dstat['DAY_WE_DS']== wk) & (dstat['ASS_ASSIGNMENT']==ass)]['MEAN'].values[0]
    prediction.append(pred)
    if (row[0]%10000 ==0):
        print(row[0])


# In[120]:

#conversion en entiers
prediction1 = [int(round(x)) for x in prediction]
for i in range(len(prediction1)):
    if prediction1[i] >100:
        prediction1[i] = 220

print(prediction1)


# In[121]:

#conversion en entiers
dsub = pd.read_csv('submission.txt', sep = "\t")
dsub['prediction'] = prediction1
print(dsub.head())



# In[122]:

dsub.to_csv("sortie.txt", sep = '\t', index = False)


# In[94]:




# In[ ]:




# In[ ]:



