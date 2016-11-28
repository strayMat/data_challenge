
# coding: utf-8
#Etienne
#Ecrit un fichier train en regroupant par attributs choisis et en rajoutant les lignes de 0 

import numpy as np
import pandas as pd


data_name = "train_2011_2012_2013.csv"
cols = ['DATE', 'ASS_ASSIGNMENT']

print("loading data...")
df = pd.read_csv(data_name, usecols = cols, sep = ";")
print("end loading\n")

from Calculhoraire import intervalle
from Calculhoraire import centre
df['TIME_SLOT']=df['DATE'].apply(lambda x:     intervalle(x))
df['ASS_ASSIGNMENT']=df['ASS_ASSIGNMENT'].apply(lambda x:     centre(x))
from datetime import datetime
df['DATE'] = df['DATE'].apply(lambda x:     datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
df['DAY_WE_DS'] = df['DATE'].dt.weekday
df['short_DATE'] = df['DATE'].dt.date

df2 = df.groupby(['short_DATE','DAY_WE_DS','ASS_ASSIGNMENT','TIME_SLOT']).size()

levels = df2.index.levels[:2] + [list(range(18)), list(range(48))]
mult = 18 * 48
labels = [
    [], [], [i for i in range(18) for j in range(48)], [j for i in range(18) for j in range(48)] ]
li = None
n = 0
for i in zip(*df2.index.labels[:2]):
    if i!=li:
        n+=1
        li = i
        labels[0] += [i[0]] * mult
        labels[1] += [i[1]] * mult
labels[2] = labels[2] * n
labels[3] = labels[3] * n
names = df2.index.names
ind3 = pd.MultiIndex(levels=levels, labels=labels, names=names)
df3 = df2.reindex(ind3, fill_value=0)

write_name = "Write_name.csv"

#Attention il faut ouvrir le fichier et renommer la dernière colonne
df3.to_csv(write_name,header=True)

