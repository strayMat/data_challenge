
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from datetime import datetime


#on charge les données préprocessées
print("loading data...")
df = pd.read_csv("train.csv", sep = ";")
print("end! ")

print(df.head())
print(len(df))

#nombre de jours qu'on regarde 
nb_days = len(np.unique(df['short_DATE']))
#nombre de semaines (144 normalement)
nb_semaines = nb_days/7
print(nb_semaines)

ass = np.unique(df.ASS_ASSIGNMENT)
print(ass)

result = pd.DataFrame({'count' : df.groupby(['ASS_ASSIGNMENT', 'DAY_WE_DS','TIME_SLOT']).size()}).reset_index()
result["MEAN"] = result["count"]/nb_semaines

#print(result[result['ASS_ASSIGNMENT']=='CAT'])
print(result)



result.to_csv("statistiques.csv")


