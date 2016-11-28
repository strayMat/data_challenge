
# coding: utf-8
#Etienne : exemple d'apprentissage sur un Decision Tree

import panda as pd

read_name = 'train.csv'
print("loading data...")
df = pd.read_csv(read_name, usecols = ['DAY_WE_DS','ASS_ASSIGNMENT','TIME_SLOT','N_Call'], sep = ",")
print("end loading\n")

Matrix = df[['DAY_WE_DS','TIME_SLOT','ASS_ASSIGNMENT']]
Result = df[['N_Call']]

from sklearn import tree
clf = tree.DecisionTreeRegressor()
clf = clf.fit(Matrix, Result)

#lit le fichier de soumission
dsub = pd.read_csv('submission.txt', sep = "\t")

from Calculhoraire import intervalle

dsub['TIME_SLOT'] =dsub['HOUR'].apply(lambda x:     intervalle(x))
dsub['DAY_WE_DS'] = dsub['DATE'].dt.weekday


#calcule ligne par ligne la prediction
prediction = []
for row in dsub.iterrows():
    ass = row[1]['ASS_ASSIGNMENT']
    time = row[1]['TIME_SLOT']
    wk = row[1]['DAY_WE_DS']
    pred = clf.predict([[centre(ass),wk,time]])
    prediction.append(pred)

#arrondit à l'entier le plus proche
from math import round
prediction = [round(x) for x in prediction]

#mise à jour
dsub['prediction']=prediction

#Ecriture
dsub.to_csv("sortie.txt", sep = '\t', index = False)



