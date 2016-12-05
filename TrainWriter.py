
# coding: utf-8

# In[5]:

import numpy as np
import pandas as pd
from Calculhoraire_exclusif import holidays
from Calculhoraire_exclusif import centre
from Calculhoraire_exclusif import intervalle


data_name = "train_2011_2012_2013.csv"
cols = ['DATE', 'ASS_ASSIGNMENT', 'CSPL_RECEIVED_CALLS']

print("loading data...")
df = pd.read_csv(data_name, usecols = cols, sep = ";")
print("end loading\n")

df['TIME_SLOT']=df['DATE'].apply(lambda x:     intervalle(x))
df['ASS_ASSIGNMENT']=df['ASS_ASSIGNMENT'].apply(lambda x:     centre(x))
from datetime import datetime
df['DATE'] = df['DATE'].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
df['DAY_WE_DS'] = df['DATE'].dt.weekday
df['short_DATE'] = df['DATE'].dt.date
df['short_DATE'] = df['short_DATE'].apply(lambda x:     datetime.strftime(x,"%Y-%m-%d"))
df['HO']=df['short_DATE'].apply(lambda x:     holidays(str(x)))
df["MONTH"] = df['short_DATE'].apply(lambda x: int(x.split("-")[1]))
df["YEAR"] = df['short_DATE'].apply(lambda x: int(x.split("-")[0]))
df["DAY"] = df['short_DATE'].apply(lambda x: int(x.split("-")[2]))

df2 = df.groupby(['short_DATE','YEAR','MONTH','DAY','DAY_WE_DS','TIME_SLOT','HO','ASS_ASSIGNMENT'])['CSPL_RECEIVED_CALLS'].sum()

write_name = "train_week_centre_time_date.csv"

#Attention il faut ouvrir le fichier et renommer la dernière colonne
df2.to_csv(write_name,header=True)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



