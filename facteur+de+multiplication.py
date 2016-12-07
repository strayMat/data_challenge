
# coding: utf-8

# In[22]:

import pandas as pd
import numpy as np
from datetime import datetime
from Calculhoraire_exclusif import centre
from math import exp

print("loading data...")
dsub = pd.read_csv("sortie.txt", sep = "\t")
print("end! ")

print("loading data...")
dreal = pd.read_csv("train_2011_2012_2013.csv", usecols = ['DATE','ASS_ASSIGNMENT','CSPL_RECEIVED_CALLS'], sep = ";")
print("end! ")


# In[23]:



# In[2]:

assignments = dreal['ASS_ASSIGNMENT'].unique()

sf = dreal.groupby(['DATE','ASS_ASSIGNMENT','CSPL_RECEIVED_CALLS'])['CSPL_RECEIVED_CALLS'].sum()

dsub['DATE'] = dsub['DATE'].apply(lambda x: datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))


# In[3]:

dreal2 = sf.to_dict()

dreal2.get(('2012-12-21 00:00:00.000','CMS'),-1)


# In[4]:


# In[24]:


errors = [np.inf for i in range(len(assignments))]

from datetime import timedelta
#on stocke le meilleur multiplicateur pour chaque assigment


# In[25]:

bestmult = [0 for i in range(len(assignments))]


# In[26]:

for i in range(5):
    tmperrors = [0 for j in range(len(assignments))]
    for row in dsub.iterrows():
        ass = row[1]['ASS_ASSIGNMENT']
        date = row[1]['DATE']
        date = date + timedelta(days=-7)
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        date+='.000'
        prediction = row[1]['prediction']
        yreal = dreal2.get((date,ass),0)
        tmperrors[centre(ass)]+=(exp(0.1*(yreal-(i+1)*prediction))-0.1*(yreal-(i+1)*prediction)-1)
    print(tmperrors)
    for a in range(len(assignments)):
        if (errors[a] > tmperrors[a]):
            errors[a] = tmperrors[a]
            bestmult[a] = i+1



# In[27]:

print(errors)
print(bestmult)


# In[28]:




# In[5]:

sum(errors)


# In[7]:

error=sum(errors)/82909
error


# In[ ]:



