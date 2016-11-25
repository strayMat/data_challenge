
# coding: utf-8

# In[1]:



import numpy as np
import pandas as pd
from Calculhoraire import intervalle
from Calculhoraire import centre

#récupération du nom des colonnes
#col_names = pd.read_csv("field_description.csv", sep = ";")['Colonne']

#col_names = [x for x in col_names]
#print(col_names)

data_name = "train_2011_2012_2013.csv"

print("loading data...")
df = pd.read_csv(data_name, usecols = ['DATE','DAY_WE_DS','ASS_ASSIGNMENT'], sep = ";")
#df = pd.read_csv(data_name,sep = ",")
print("end loading\n")


# In[2]:

df['TIME_SLOT'] = df['DATE'].apply(lambda x:     intervalle(x))
df['ASS_ASSIGNMENT'] = df['ASS_ASSIGNMENT'].apply(lambda x:     centre(x))
from datetime import datetime
df["DATE"] = df["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))

df['TIME'] = df['DATE'].dt.time
#df['short_DATE'] = df['DATE'].dt.date
df['DAY_NUM'] = df['DATE'].dt.weekday


# In[3]:

df = df.drop('TIME', axis=1)
df = df.drop('DAY_WE_DS', axis=1)


# In[4]:

cols = df.columns.tolist()
cols = cols[:1] + cols[-1:] + cols[-2:-1]+ cols[1:-2]
print(cols)
df = df[cols]
df['N_Call'] = 1
print(df.head())


# In[5]:

df2 = df
df2['N_Call'] = df2['N_Call'].groupby(df['DATE']).transform('sum')


# In[205]:

print(df2.head())

df2.to_csv('train.csv', sep =',')


# In[ ]:



