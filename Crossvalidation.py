
# coding: utf-8

# In[85]:


from datetime import datetime
import pandas as pd
from Calculhoraire_exclusif import intervalle
from Calculhoraire_exclusif import centre
from Calculhoraire_exclusif import holidays
from Calculhoraire_exclusif import inverse
from sklearn.tree import DecisionTreeRegressor
from sklearn.utils import shuffle
from math import exp
from sklearn import ensemble
import numpy as np
from math import ceil

read_name = 'train_week_centre_time_date.csv'
print("loading data...")
df = pd.read_csv(read_name, sep = ",")
print("end loading\n")

df['WEEK_END']=df['DAY_WE_DS'].apply(lambda x:     int(x>=5))

print(df.head())
print(len(df))


# In[86]:

#limits for each assignment
#limits=[300,1,1,70,0,3,70,0,12,5,4,7,0,12,5,10,55,80,2,14,70,25,15,100,425,120,120,1400]
limits = [0 for i in range(28)]
for i in range(28):
    limits[i]=df[(df.ASS_ASSIGNMENT==i) & ((df.YEAR>2012) | ((df.YEAR==2012) & (df.MONTH>=6)))].CSPL_RECEIVED_CALLS.max(axis=0)
    
print(limits)

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



# In[87]:

df = df[df["ASS_ASSIGNMENT"]!= 4]


assign = np.unique(df.ASS_ASSIGNMENT)
print(assign)


# In[88]:

[inverse(x) for x in assign]


# In[99]:


#je crée un subsample de mon dataset surlequel train et un autre pour tester
df = shuffle(df) 
offset = int(df.shape[0] * 0.9)
X = df[["ASS_ASSIGNMENT","YEAR","MONTH", "DAY", "TIME_SLOT", "HO", 'DAY_WE_DS', "WEEK_END"]]
Y = df[["ASS_ASSIGNMENT","CSPL_RECEIVED_CALLS"]]
X_train, Y_train = X[:offset], Y[:offset]
X_test, Y_test = X[offset:], Y[offset:]


# In[100]:

param = [{'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 8}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 8}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}, {'learning_rate': 0.1, 'max_depth': 4}, {'learning_rate': 0.01, 'max_depth': 4}]

clf = [0 for x in range(28)]
for i in assign:
    clf[i] = ensemble.GradientBoostingRegressor(loss='ls', n_estimators=n_iterations[i], max_depth = param[0]['max_depth'], learning_rate = param[i]['learning_rate'], verbose=1, presort='auto')


# In[101]:


for i in assign:
    Matrix = X_train[X_train["ASS_ASSIGNMENT"]==i]
    Matrix = Matrix[['YEAR','MONTH','DAY','TIME_SLOT','HO','DAY_WE_DS','WEEK_END']]
    Result = Y_train[Y_train['ASS_ASSIGNMENT']==i]
    #Result['CSPL_RECEIVED_CALLS'] = Result['CSPL_RECEIVED_CALLS'].apply(lambda x: exp(x))
    Result = Result['CSPL_RECEIVED_CALLS']
    print(inverse(i))
    clf[i].fit(Matrix, Result)



# In[102]:

prediction = []
for row in X_test.iterrows():
    ass = row[1]['ASS_ASSIGNMENT']
    if limits[centre(ass)] == 0:
        prediction.append(0)
        continue
    time = row[1]['TIME_SLOT']
    wk = row[1]['WEEK_END']
    dayds = row[1]['DAY_WE_DS']
    month = row[1]['MONTH']
    year = row[1]['YEAR']
    day = row[1]['DAY']
    holidays = row[1]['HO']
    pred = clf[centre(ass)].predict([[year,month,day,time,holidays,dayds,wk]])
    pred = max(0,pred)       
    pred = min(limits[centre(ass)]/2,pred)
    #pred = 2*pred
    prediction.append(pred)

#arrondit à l'entier le plus proche
prediction = [int(x) for x in prediction]


# In[ ]:




# In[103]:

error = 0
for row in Y_test.iterrows():
    yreal = row[1]["CSPL_RECEIVED_CALLS"]
    error += (exp(0.1*(yreal-prediction[i]))-0.1*(yreal-prediction[i])-1)
error = error/len(Y_test)
print(error)


# In[ ]:



