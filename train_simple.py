
# coding: utf-8

# In[136]:

import numpy as np
import pandas as pd
from Calculhoraire import intervalle

#récupération du nom des colonnes
#col_names = pd.read_csv("field_description.csv", sep = ";")['Colonne']

#col_names = [x for x in col_names]
#print(col_names)


# In[200]:

data_name = "train_2011_2012_2013.csv"

print("loading data...")
df = pd.read_csv(data_name, usecols = ['DATE','DAY_WE_DS','ASS_ASSIGNMENT'], sep = ";")
#df = pd.read_csv(data_name,sep = ",")
print("end loading\n")


# In[201]:

#conversion en format pandas date de la colonne date
from datetime import datetime
df["DATE"] = df["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))

df['TIME'] = df['DATE'].dt.time
#df['short_DATE'] = df['DATE'].dt.date
#df['DAY_NUM'] = df['DATE'].date.weekday()
df['TIME_SLOT'] = df['TIME'].apply(lambda x: intervalle(x))

df = df.drop('DATE', axis=1)
df = df.drop('TIME', axis=1)
df = df.drop('DAY_WE_DS', axis=1)
df = df.drop('ASS_ASSIGNMENT', axis=1)
# we only keep the features of interest : day, time slot and number of calls


# In[202]:

cols = df.columns.tolist()
cols = cols[:1] + cols[-1:] + cols[-2:-1]+ cols[1:-2]
print(cols)
df = df[cols]
df['N_Call'] = 1
print(df.head())






# In[204]:

df2 = df
df2['N_Call'] = df2['N_Call'].groupby(df['DATE']).transform('sum')


# In[205]:

print(df2.head())

df2.to_csv('train.csv', sep =',')




