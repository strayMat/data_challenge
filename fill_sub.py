
# coding: utf-8

# In[8]:

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import Calculhoraire as chor

sub_name = "submission_tab.txt"
#toutes les colonnes
#cols = list(['DATE', 'DAY_OFF', 'DAY_DS', 'WEEK_END', 'DAY_WE_DS', 'TPER_TEAM', 'TPER_HOUR', 'SPLIT_COD', 'ACD_COD', 'ACD_LIB', 'ASS_SOC_MERE', 'ASS_DIRECTORSHIP', 'ASS_ASSIGNMENT', 'ASS_PARTNER', 'ASS_POLE', 'ASS_BEGIN', 'ASS_END', 'ASS_COMENT', 'CSPL_I_STAFFTIME', 'CSPL_I_AVAILTIME', 'CSPL_I_ACDTIME', 'CSPL_I_ACWTIME', 'CSPL_I_ACWOUTTIME', 'CSPL_I_ACWINTIME', 'CSPL_I_AUXOUTTIME', 'CSPL_I_AUXINTIME', 'CSPL_I_OTHERTIME', 'CSPL_ACWINCALLS', 'CSPL_ACWINTIME', 'CSPL_AUXINCALLS', 'CSPL_AUXINTIME', 'CSPL_ACWOUTCALLS', 'CSPL_ACWOUTIME', 'CSPL_ACWOUTOFFCALLS', 'CSPL_ACWOUTOFFTIME', 'CSPL_AUXOUTCALLS', 'CSPL_AUXOUTTIME', 'CSPL_AUXOUTOFFCALLS', 'CSPL_AUXOUTOFFTIME', 'CSPL_INFLOWCALLS', 'CSPL_ACDCALLS', 'CSPL_ANSTIME', 'CSPL_HOLDCALLS', 'CSPL_HOLDTIME', 'CSPL_HOLDABNCALLS', 'CSPL_TRANSFERED', 'CSPL_CONFERENCE', 'CSPL_ABNCALLS', 'CSPL_ABNTIME', 'CSPL_ABNCALLS1', 'CSPL_ABNCALLS2', 'CSPL_ABNCALLS3', 'CSPL_ABNCALLS4', 'CSPL_ABNCALLS5', 'CSPL_ABNCALLS6', 'CSPL_ABNCALLS7', 'CSPL_ABNCALLS8', 'CSPL_ABNCALLS9', 'CSPL_ABNCALLS10', 'CSPL_OUTFLOWCALLS', 'CSPL_OUTFLOWTIME', 'CSPL_MAXINQUEUE', 'CSPL_CALLSOFFERED', 'CSPL_I_RINGTIME', 'CSPL_RINGTIME', 'CSPL_RINGCALLS', 'CSPL_NOANSREDIR', 'CSPL_MAXSTAFFED', 'CSPL_ACWOUTADJCALLS', 'CSPL_AUXOUTADJCALLS', 'CSPL_DEQUECALLS', 'CSPL_DEQUETIME', 'CSPL_DISCCALLS', 'CSPL_DISCTIME', 'CSPL_INTRVL', 'CSPL_INCOMPLETE', 'CSPL_ACCEPTABLE', 'CSPL_SERVICELEVEL', 'CSPL_ACDAUXOUTCALLS', 'CSPL_SLVLABNS', 'CSPL_SLVLOUTFLOWS', 'CSPL_RECEIVED_CALLS', 'CSPL_ABANDONNED_CALLS', 'CSPL_CALLS', 'CSPL_ACWTIME', 'CSPL_ACDTIME'])
#les colonnes à enlever
#cols_to_drop = ['ASS_END','ASS_BEGIN', 'DAY_WE_DS']
#les colonnes catégorielles à modifier en int 
#cols_str = ['ASS_POLE', 'ASS_PARTNER', 'ASS_ASSIGNMENT', 'ASS_DIRECTORSHIP', 'ASS_SOC_MERE', 'ACD_LIB', 'TPER_TEAM']
#on drop les colonnes qu'on ne veut pas 
#cols = [x for x in cols if x not in cols_to_drop]
#cols = cols[:14]
#print(cols)
print("loading data...")
#attention retirer nrows pour sortir le fichier complet (moi ça fait bugger jupyter et je dois eteindre mon PC)
df = pd.read_csv(sub_name, sep = "\t")#, nrows = 100000)
print("end loading\n")

data_name = "train.csv"

print("loading real data...")
data = pd.read_csv(data_name, usecols = ['DAY_WE_DS','TIME_SLOT','ASS_ASSIGNMENT','N_Call'], sep = ";")
#df = pd.read_csv(data_name,sep = ",")
print("end loading\n")
#print(data[0:2])


# In[7]:
print(data.head())
Matrix = data[['DAY_WE_DS','TIME_SLOT','ASS_ASSIGNMENT']]
Result = data[['N_Call']]

print(Matrix.head())
print(Result.head())

# In[8]:

from sklearn import tree
clf = tree.DecisionTreeRegressor()
clf = clf.fit(Matrix, Result)


# In[9]:

#print(df.head())
#print (len(df))

for i in range (len(df)):
    line = df.values[i,:]
    date_str = line[0]+" "+line[1]
    #print(date_str)
    date = datetime.strptime(date_str,"%Y-%m-%d %H:%M:%S.%f")
    weekday = date.weekday()
    #print(weekday)
    time_slot = chor.intervalle(date_str)
    Nb_ass = chor.centre(line[2])
    #print(Nb_ass)
    
    df[i,3] = clf.predict([[weekday, time_slot, Nb_ass]])[0]
    #print(type(clf.predict([[weekday, time_slot, Nb_ass]])[0]))
    #print(df[i,3])

    print (i)
    
print("ecriture du fichier sortie")
df.to_csv('sortie.csv', sep =';', index = False)
print("end!")
    