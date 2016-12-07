
# coding: utf-8

# In[20]:

from datetime import datetime
import pandas as pd
from Calculhoraire_exclusif import intervalle
from Calculhoraire_exclusif import centre
from Calculhoraire_exclusif import holidays
from Calculhoraire_exclusif import inverse

from sklearn.tree import DecisionTreeRegressor
from sklearn import ensemble
from sklearn.model_selection import GridSearchCV
import numpy as np
from math import exp
from math import log
from math import ceil


read_name = 'train_week_centre_time_date.csv'
print("loading data...")
df = pd.read_csv(read_name, sep = ",")
print("end loading\n")
#df['WEEK_END']=df['DAY_WE_DS'].apply(lambda x:     int(x>=5))


# In[13]:

print(df.head())


# In[14]:

assign = np.unique(df.ASS_ASSIGNMENT)
print(assign)
#des limites pour couper à la fin si on a prévu trop 
limits = [0 for i in range(28)]
for i in range(28):
    limits[i]=df[(df.ASS_ASSIGNMENT==i) & ((df.YEAR>2012) | ((df.YEAR==2012) & (df.MONTH>=6)))].CSPL_RECEIVED_CALLS.max(axis=0)
    


# In[15]:

n_iterations=[0 for i in range(28)]
for i in range(28):
    if limits[i]>=80:
        n_iterations[i]=1000
    elif limits[i]>=40:
        n_iterations[i]=500
    elif limits[i]>=20:
        n_iterations[i]=200
    else:
        n_iterations[i]=70
print(len(limits))
print(len(n_iterations))


# In[16]:

clf = []
param = []
for i in assign:
    #clf.append(DecisionTreeRegressor())
    #clf.append(ensemble.GradientBoostingRegressor(loss='ls', learning_rate=0.1, n_estimators=500, subsample=1.0, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_depth=3, init=None, random_state=None, max_features=None, alpha=0.96, verbose=0, max_leaf_nodes=None, warm_start=False, presort='auto'))
    clf.append(ensemble.GradientBoostingRegressor(loss = 'ls', n_estimators=n_iterations[i],verbose = 1, presort = 'auto'))


# In[21]:

inverse(15)


# In[17]:

#on test divers paramatres : 
#Attention très très long, notamment parceque learning rate très bas je pense
param_grid = {"learning_rate": [0.1, 0.01],
"max_depth": [4,8]}

print("cross_fitting")
for i in assign:
    Matrix = df[df["ASS_ASSIGNMENT"]==i]
    Matrix = Matrix[['DAY_WE_DS','TIME_SLOT','MONTH','YEAR','DAY','HO']]
    Result = df[df['ASS_ASSIGNMENT']==i]
    #Result['CSPL_RECEIVED_CALLS'] = Result['CSPL_RECEIVED_CALLS'].apply(lambda x: exp(x))
    Result = Result['CSPL_RECEIVED_CALLS']
    print(i)
    gs_cv = GridSearchCV(clf[i], param_grid).fit(Matrix, Result)
    param.append(gs_cv.best_params_)
print("end fitting")


# In[ ]:




# In[36]:

#pour eviter de relancer la gridsearch voici les parametres obtenus en le faisant tourner
param = [{'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 8}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 8}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}]
print(param)


# In[33]:

#On recree les classifieurs avec les bons parametres
clf = []
for i in assign:
    clf.append(ensemble.GradientBoostingRegressor(loss = 'ls', n_estimators=n_iterations[i], max_depth = param[0]['max_depth'], learning_rate = param[i]['learning_rate'], verbose = 1, presort = 'auto'))


# In[ ]:




# In[34]:

print("fitting")
for i in assign:
    Matrix = df[df["ASS_ASSIGNMENT"]==i]
    Matrix = Matrix[['DAY_WE_DS','TIME_SLOT','MONTH','YEAR','DAY','HO']]
    Result = df[df['ASS_ASSIGNMENT']==i]
    #Result['CSPL_RECEIVED_CALLS'] = Result['CSPL_RECEIVED_CALLS'].apply(lambda x: exp(x))
    Result = Result['CSPL_RECEIVED_CALLS']
    clf[i].fit(Matrix, Result)
print("end fitting")


# In[ ]:




# In[35]:

dsub = pd.read_csv('submission.txt', sep = "\t")
print(dsub.head())
print("convert to timestamp...")
dsub["DATE"] = dsub["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
dsub["short_DATE"] = dsub["DATE"].apply(lambda x:     datetime.strftime(x,"%Y-%m-%d"))
dsub['HO'] = dsub['short_DATE'].apply(lambda x: holidays(x))
print("End of conversion!")


dsub['DAY_WE_DS'] = dsub['DATE'].dt.weekday
dsub['DAY'] = dsub['DATE'].dt.day
dsub['MONTH'] = dsub['DATE'].dt.month
dsub['YEAR'] = dsub['DATE'].dt.year
dsub['TIME_SLOT'] =dsub['DATE'].apply(lambda x: intervalle(x))


# In[ ]:

prediction = []
for row in dsub.iterrows():
    ass = row[1]['ASS_ASSIGNMENT']
    time = row[1]['TIME_SLOT']
    wk = row[1]['DAY_WE_DS']
    month = row[1]['MONTH']
    year = row[1]['YEAR']
    day = row[1]['DAY']
    holidays = row[1]['HO']
    pred = clf[centre(ass)].predict([[wk,time,month,year,day,holidays]])
    prediction.append(max(0,pred))

#arrondit à l'entier le plus proche
prediction = [int(x) for x in prediction]

#mise à jour
dsub['prediction']=prediction
dsub['DATE']=dsub['DATE'].apply(lambda x:     datetime.strftime(x,"%Y-%m-%d %H:%M:%S"))
dsub['DATE']=dsub['DATE']+'.000'
header = ['DATE', 'ASS_ASSIGNMENT', 'prediction']
#Ecriture
dsub.to_csv("sortie.txt", columns = header, sep = '\t', index = False)


# In[ ]:





# In[ ]:



