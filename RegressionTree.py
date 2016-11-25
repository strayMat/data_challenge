
# coding: utf-8

# In[5]:



import numpy as np
import pandas as pd
from Calculhoraire import intervalle
from Calculhoraire import centre

#récupération du nom des colonnes
data_name = "train.csv"

#col_names = pd.read_csv(data_name, sep = ",")['Colonne']

#col_names = [x for x in col_names]
#print(col_names)


print("loading data...")
df = pd.read_csv(data_name, usecols = ['DAY_NUM','TIME_SLOT','ASS_ASSIGNMENT','N_Call'], sep = ",")
#df = pd.read_csv(data_name,sep = ",")
print("end loading\n")
print(df[0:2])


# In[7]:

Matrix = df[['DAY_NUM','TIME_SLOT','ASS_ASSIGNMENT']]
Result = df[['N_Call']]


# In[8]:

from sklearn import tree
clf = tree.DecisionTreeRegressor()
clf = clf.fit(Matrix, Result)


# In[9]:

print(clf.predict([[6, 3, 17]]))


# In[10]:

print(clf.predict([[6, 3, 11]]))


# In[11]:

print(clf.predict([[6, 3, 5]]))


# In[ ]:



