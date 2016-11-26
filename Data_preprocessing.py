
# coding: utf-8

# In[8]:

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from Calculhoraire import intervalle

data_name = "train_2011_2012_2013.csv"
#toutes les colonnes
cols = list(['DATE', 'DAY_OFF', 'DAY_DS', 'WEEK_END', 'DAY_WE_DS', 'TPER_TEAM', 'TPER_HOUR', 'SPLIT_COD', 'ACD_COD', 'ACD_LIB', 'ASS_SOC_MERE', 'ASS_DIRECTORSHIP', 'ASS_ASSIGNMENT', 'ASS_PARTNER', 'ASS_POLE', 'ASS_BEGIN', 'ASS_END', 'ASS_COMENT', 'CSPL_I_STAFFTIME', 'CSPL_I_AVAILTIME', 'CSPL_I_ACDTIME', 'CSPL_I_ACWTIME', 'CSPL_I_ACWOUTTIME', 'CSPL_I_ACWINTIME', 'CSPL_I_AUXOUTTIME', 'CSPL_I_AUXINTIME', 'CSPL_I_OTHERTIME', 'CSPL_ACWINCALLS', 'CSPL_ACWINTIME', 'CSPL_AUXINCALLS', 'CSPL_AUXINTIME', 'CSPL_ACWOUTCALLS', 'CSPL_ACWOUTIME', 'CSPL_ACWOUTOFFCALLS', 'CSPL_ACWOUTOFFTIME', 'CSPL_AUXOUTCALLS', 'CSPL_AUXOUTTIME', 'CSPL_AUXOUTOFFCALLS', 'CSPL_AUXOUTOFFTIME', 'CSPL_INFLOWCALLS', 'CSPL_ACDCALLS', 'CSPL_ANSTIME', 'CSPL_HOLDCALLS', 'CSPL_HOLDTIME', 'CSPL_HOLDABNCALLS', 'CSPL_TRANSFERED', 'CSPL_CONFERENCE', 'CSPL_ABNCALLS', 'CSPL_ABNTIME', 'CSPL_ABNCALLS1', 'CSPL_ABNCALLS2', 'CSPL_ABNCALLS3', 'CSPL_ABNCALLS4', 'CSPL_ABNCALLS5', 'CSPL_ABNCALLS6', 'CSPL_ABNCALLS7', 'CSPL_ABNCALLS8', 'CSPL_ABNCALLS9', 'CSPL_ABNCALLS10', 'CSPL_OUTFLOWCALLS', 'CSPL_OUTFLOWTIME', 'CSPL_MAXINQUEUE', 'CSPL_CALLSOFFERED', 'CSPL_I_RINGTIME', 'CSPL_RINGTIME', 'CSPL_RINGCALLS', 'CSPL_NOANSREDIR', 'CSPL_MAXSTAFFED', 'CSPL_ACWOUTADJCALLS', 'CSPL_AUXOUTADJCALLS', 'CSPL_DEQUECALLS', 'CSPL_DEQUETIME', 'CSPL_DISCCALLS', 'CSPL_DISCTIME', 'CSPL_INTRVL', 'CSPL_INCOMPLETE', 'CSPL_ACCEPTABLE', 'CSPL_SERVICELEVEL', 'CSPL_ACDAUXOUTCALLS', 'CSPL_SLVLABNS', 'CSPL_SLVLOUTFLOWS', 'CSPL_RECEIVED_CALLS', 'CSPL_ABANDONNED_CALLS', 'CSPL_CALLS', 'CSPL_ACWTIME', 'CSPL_ACDTIME'])
#les colonnes à enlever
cols_to_drop = ['ASS_END','ASS_BEGIN', 'DAY_WE_DS']
#les colonnes catégorielles à modifier en int 
cols_str = ['ASS_POLE', 'ASS_PARTNER', 'ASS_ASSIGNMENT', 'ASS_DIRECTORSHIP', 'ASS_SOC_MERE', 'ACD_LIB', 'TPER_TEAM']
#on drop les colonnes qu'on ne veut pas 
cols = [x for x in cols if x not in cols_to_drop]
cols = cols[:14]
print(cols)
print("loading data...")
#attention retirer nrows pour sortir le fichier complet (moi ça fait bugger jupyter et je dois eteindre mon PC)
df = pd.read_csv(data_name, usecols = cols, sep = ";", nrows = 100000)
print("end loading\n")


# In[9]:


le = LabelEncoder()
#on gere les données catégorielles (ces petites putes)
for x in cols_str:
    df[x] = df[x].astype('category')
    le.fit(df[x])
    df[x] = le.transform(df[x])


# In[10]:



#conversion en format pandas date de la colonne date
df['TIME_SLOT'] = df['DATE'].apply(lambda x:     intervalle(x))
print("Convert date format...")
from datetime import datetime
df["DATE"] = df["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))

#création de colonne time et short_date, conversion des jours de la semaine en numéro
df['TIME'] = df['DATE'].dt.time
df['short_DATE'] = df['DATE'].dt.date
df['DAY_WE_DS'] = df['DATE'].dt.weekday
print("end conversion")


# In[92]:




# In[11]:

# In[202]:
#Reorganisation "à la main" des colonnes 
cols = df.columns.tolist()
cols = cols[:1] + cols[-2:-1] +  cols[-3:-2] + cols[-4:-3] + cols[-1:] + cols[1:-4]
#print(cols)
df = df[cols]
df['N_Call'] = 1
print(df.head())


# In[12]:

#grouper par date complete (jour et heure) et indiquer le nombre d'appel dans cette tranche ci 
df2 = df
df2['N_Call'] = df2['N_Call'].groupby(df['DATE']).transform('sum')


# In[205]:

print(df2.head())

print("ecriture du fichier sortie")
df2.to_csv('train.csv', sep =';', index = False)
print("end!")


# In[ ]:



