
# coding: utf-8

# In[46]:

import pandas as pd
import numpy as np
from datetime import datetime
from Calculhoraire import inverseCentre
import plotly.plotly as py
import matplotlib.pyplot as plt

#on charge les données préprocessées
print("loading data...")
df = pd.read_csv("Train_ass_timeslot_centre.csv", sep = ",")
print("end! ")


# In[47]:

df['ASS_ASSIGNMENT'] = df.ASS_ASSIGNMENT.apply(lambda x: inverseCentre(x))
print(df)


# In[48]:

#convert to timestamps and get mont number
#df["DATE"] = df["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))
df["MONTH"] = df['short_DATE'].apply(lambda x: int(x.split("-")[1]))
df["YEAR"] = df['short_DATE'].apply(lambda x: int(x.split("-")[0]))
df["DAY"] = df['short_DATE'].apply(lambda x: int(x.split("-")[2]))
print(df.head())
print(len(df))


# In[95]:

#plot les graphiques sur une semaine pour chaque assignment center
ass = np.unique(df["ASS_ASSIGNMENT"])
for a in ass:
    y = df[(df["ASS_ASSIGNMENT"]==str(a)) & (df['YEAR']<=2013)&(df['MONTH']<13)]['N_Call']
    x = range(len(y))
    str_a = a.decode("ascii", "ignore")
    line = plt.figure()
    plt.plot(x,y,"o")
    plt.title("nombre appels pour le centre : " + str_a + " au cours de la periode")
    #plt.show()
    plt.savefig('period_scatterplot/period_of_'+str(a)+'.png')
    plt.clf()
    plt.close()
    


# In[ ]:



