
# coding: utf-8

# In[107]:

from datetime import datetime
import pandas as pd
from Calculhoraire_exclusif import intervalle
from Calculhoraire_exclusif import centre
from sklearn import tree
import numpy as np


read_name = 'train_assignment_date_timeslot_wkday.csv'
print("loading data...")
df = pd.read_csv(read_name, sep = ",")
print("end loading\n")


# In[108]:

df["MONTH"] = df['short_DATE'].apply(lambda x: int(x.split("-")[1]))
df["YEAR"] = df['short_DATE'].apply(lambda x: int(x.split("-")[0]))
df["DAY"] = df['short_DATE'].apply(lambda x: int(x.split("-")[2]))
print(df.head())
print(len(df))


# In[109]:

assign = np.unique(df.ASS_ASSIGNMENT)
print(assign)


# In[111]:

clf = []
for i in assign:
    clf.append(tree.DecisionTreeRegressor())
for i in assign:
    Matrix = df[df["ASS_ASSIGNMENT"]==i]
    Matrix = Matrix[['DAY_WE_DS','TIME_SLOT','MONTH','YEAR']]
    Result = df[df['ASS_ASSIGNMENT']==i]
    Result = Result['0']   
    clf[i].fit(Matrix, Result)


# In[ ]:




# In[112]:

#lit le fichier de soumission
dsub = pd.read_csv('submission.txt', sep = "\t")
print(dsub.head())
print("convert to timestamp...")
dsub["DATE"] = dsub["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
print("End of conversion!")


dsub['DAY_WE_DS'] = dsub['DATE'].dt.weekday
dsub['MONTH'] = dsub['DATE'].dt.month
dsub['YEAR'] = dsub['DATE'].dt.year
dsub['TIME_SLOT'] =dsub['DATE'].apply(lambda x:     intervalle(x))


# In[114]:

#calcule ligne par ligne la prediction
prediction = []
for row in dsub.iterrows():
    ass = row[1]['ASS_ASSIGNMENT']
    time = row[1]['TIME_SLOT']
    wk = row[1]['DAY_WE_DS']
    month = row[1]['MONTH']
    year = row[1]['YEAR']
    pred = clf[centre(ass)].predict([[wk,time,month,year]])
    prediction.append(pred)

#arrondit à l'entier le plus proche
prediction = [int(x) for x in prediction]

#mise à jour
dsub['prediction']=prediction
header = ['DATE', 'ASS_ASSIGNMENT', 'prediction']
#Ecriture
dsub.to_csv("sortie.txt", columns = header, sep = '\t', index = False)



# In[22]:




# In[ ]:



