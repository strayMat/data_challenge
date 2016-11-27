
# coding: utf-8

# In[35]:

import pandas as pd
import numpy as np
from datetime import datetime


#on charge les données préprocessées
print("loading data...")
df = pd.read_csv("train.csv", sep = ";")
print("end! ")

#convert to timestamps and get mont number
#df["DATE"] = df["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))
#df["MONTH"] = df["DATE"].dt.month

print(df.head())
print(len(df))


# In[55]:

#nombre de jours qu'on regarde 
nb_days = len(np.unique(df['short_DATE']))
#nombre de semaines (144 normalement)
nb_semaines = nb_days/7
print(nb_semaines)

ass = np.unique(df.ASS_ASSIGNMENT)
print(ass)


# In[84]:

result = pd.DataFrame({'count' : df.groupby(['ASS_ASSIGNMENT', 'DAY_WE_DS','TIME_SLOT']).size()}).reset_index()
result["MEAN"] = result["count"]/nb_semaines

#print(result[result['ASS_ASSIGNMENT']=='CAT'])
print(result)


# In[88]:



#plot les graphiques sur une semaine pour chaque assignment center
import plotly.plotly as py
import matplotlib.pyplot as plt

#créer les abcisses pour le weekplot
result['WK_TIME_SLOT'] = result['TIME_SLOT'] + 48*result['DAY_WE_DS']

for a in ass:
    a_ass = result[result.ASS_ASSIGNMENT == str(a)]

    x = list(a_ass.WK_TIME_SLOT)
    y = list(a_ass.MEAN)
    str_a = a.decode("ascii", "ignore")
    line = plt.figure()
    plt.plot(x,y)
    plt.title("nombre appels pour le centre : " + str_a + " au cours de la semaine")
    #plt.show()
    plt.savefig('week_scatterplot/week_of_'+str(a)+'.png')
    plt.clf()
    


# In[70]:




# In[83]:




# In[ ]:



