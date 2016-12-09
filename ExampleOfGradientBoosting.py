
# coding: utf-8

# In[1]:
#best parameters found with a grid search
param = [{'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 250, 'subsample': 1.0}, 
         {'learning_rate': 0.01, 'max_depth': 3, 'n_estimators': 250, 'subsample': 1.0},
         {'learning_rate': 0.01, 'max_depth': 1, 'n_estimators': 100, 'subsample': 1.0}, 
         {'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 500, 'subsample': 0.9}, 
         {'learning_rate': 0.01, 'max_depth': 3, 'n_estimators': 250, 'subsample': 1.0}, 
         {'learning_rate': 0.01, 'max_depth': 1, 'n_estimators': 100, 'subsample': 1.0}, 
         {'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 250, 'subsample': 1.0},
         {'learning_rate': 0.01, 'max_depth': 1, 'n_estimators': 100, 'subsample': 1.0}, 
         {'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 250, 'subsample': 0.9}, 
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 250, 'subsample': 0.9}, 
         {'learning_rate': 0.01, 'max_depth': 3, 'n_estimators': 500, 'subsample': 1.0}, 
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 250, 'subsample': 0.9}, 
         {'learning_rate': 0.1, 'max_depth': 1, 'n_estimators': 100, 'subsample': 0.9}, 
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 100, 'subsample': 0.9},
         {'learning_rate': 0.01, 'max_depth': 3, 'n_estimators': 500, 'subsample': 0.9}, 
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 500, 'subsample': 0.9}, 
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 500, 'subsample': 0.9}, 
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 100, 'subsample': 0.9},
         {'learning_rate': 0.01, 'max_depth': 3, 'n_estimators': 250, 'subsample': 0.9}, 
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 500, 'subsample': 0.9}, 
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 500, 'subsample': 0.9}, 
         {'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 100, 'subsample': 0.9}, 
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 500, 'subsample': 0.9},
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 500, 'subsample': 0.9}, 
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 500, 'subsample': 0.9}, 
         {'learning_rate': 0.1, 'max_depth': 6, 'n_estimators': 100, 'subsample': 0.9},
         {'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 500, 'subsample': 1.0},
         {'learning_rate': 0.1, 'max_depth': 6, 'n_estimators': 250, 'subsample': 1.0}]


# In[ ]:

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
from math import ceil
import time

start_time = time.time()

#Having weeks to be predicted
predict_intervals = pd.read_csv('predict_weeks/intervals.csv', sep=';')

predict_intervals = predict_intervals.as_matrix()

for w in range(12):

    read_name = 'train/'+str(w)+'/train_week_centre_time_date.csv'
    print("loading data...")
    df = pd.read_csv(read_name, sep = ",")
    print("end loading\n")
    
    df['WEEK_END']=df['DAY_WE_DS'].apply(lambda x:     int(x>=5))
    
    print(df.head())
    print(len(df))
    
    #limits for each assignment from the start to the week w
    limits = [[0 for k in range(28)] for v in range(12)]
    #finding maximal value and average value
    for i in range(28):
        limits[w][i]=df[(df.ASS_ASSIGNMENT==i)].CSPL_RECEIVED_CALLS.max(axis=0)
    
    #0 special case for Evenements
    limits[centre('Evenements')][w]=0
    
    assign = np.unique(df.ASS_ASSIGNMENT)
    
    print('end !')
    print(time.time()-start_time)
    start_time = time.time()
    
    # In[ ]:
    #start of training
    clf = [[] for i in range(12)]
    for i in assign:
        clf[w].append(ensemble.GradientBoostingRegressor(loss='ls', max_depth = param[i]['max_depth'], 
                                                      learning_rate = param[i]['learning_rate'], 
                                                      n_estimators=param[i]['n_estimators'], 
                                                      criterion='friedman_mse', 
                                                      subsample=param[i]['subsample'], 
                                                      init=None, 
                                                      random_state=None, 
                                                      max_features=None, 
                                                      verbose=0, 
                                                      max_leaf_nodes=None, 
                                                      warm_start=False, 
                                                      presort='auto'))
    
    for i in assign:
        Matrix = df[df["ASS_ASSIGNMENT"]==i]
        Matrix = Matrix[['YEAR','MONTH','DAY','TIME_SLOT','DAY_WE_DS','WEEK_END']]
        Result = df[df['ASS_ASSIGNMENT']==i]
        Result = Result['CSPL_RECEIVED_CALLS']
        print(inverse(i))
        clf[w][i].fit(Matrix, Result)
#end of training

# In[ ]:
start = '2011-01-01 00:00:00.000'
start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
#reading the submission file
dsub = pd.read_csv('submission/submission.txt', sep = "\t")
print(dsub.head())
print("convert to timestamp...")
dsub["DATE"] = dsub["DATE"].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
dsub["short_DATE"] = dsub["DATE"].apply(lambda x:     datetime.strftime(x,"%Y-%m-%d"))
dsub['HO'] = dsub['short_DATE'].apply(lambda x: holidays(x))

dsub["ABSOLUTE"] = dsub['DATE'].apply(lambda x:     ((x-start).days)*48)

dsub['DAY_WE_DS'] = dsub['DATE'].dt.weekday
dsub['WEEK_END'] = dsub['DAY_WE_DS'].apply(lambda x:     int(x>=5))
dsub['DAY'] = dsub['DATE'].dt.day
dsub['MONTH'] = dsub['DATE'].dt.month
dsub['YEAR'] = dsub['DATE'].dt.year
dsub['TIME_SLOT'] =dsub['DATE'].apply(lambda x: intervalle(x))
print("End of conversion!")


# In[ ]:
#prediction
prediction = []
for row in dsub.iterrows():
    ass = row[1]['ASS_ASSIGNMENT']
    time = row[1]['TIME_SLOT']
    wk = row[1]['WEEK_END']
    dayds = row[1]['DAY_WE_DS']
    month = row[1]['MONTH']
    year = row[1]['YEAR']
    day = row[1]['DAY']
    #finding which regressor we can use given the data    
    ABSOLUTE = row[1]['ABSOLUTE']
    w = 0
    while ABSOLUTE>predict_intervals[w][0]:
        w+=1
    #now we have the right dataset to predict on
    
    pred = clf[w][centre(ass)].predict([[year,month,day,time,dayds,wk]])
    pred = max(0,pred)
    pred = min(limits[w][centre(ass)]*1.1, 1.56*pred)
        
    prediction.append(pred)

#round to nearest integer
prediction = [int(x) for x in prediction]

dsub['DATE']=dsub['DATE'].apply(lambda x:     datetime.strftime(x,"%Y-%m-%d %H:%M:%S"))
dsub['DATE']=dsub['DATE']+'.000'


# In[ ]:
#writing submission
header = ['DATE', 'ASS_ASSIGNMENT', 'prediction']
#mise à jour
dsub['prediction']=prediction
#Ecriture
dsub.to_csv("submission/sortie.txt", columns = header, sep = '\t', index = False)
