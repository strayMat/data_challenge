# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:49:03 2016

@author: etienne
"""
import pandas as pd

def assignementNumber(X):
    col_names = pd.read_csv("field_description.csv", sep = ",")['Colonne']

def intervalle(X):
   x = str(X).split()[1].split(':')
   return int(x[0])*2 + (int(x[1])==30)

def jour(X):
    #Date format AAAA-MM-JJ
    start = 6 #1 janvier 2011 = Samedi 6 ème jour semaine
    
    mois = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    annee = ord(X[3])-48
    
    moistotal = (ord(X[5])-48)*10+(ord(X[6])-48)
    
    jourmois = (ord(X[8])-48)*10+(ord(X[9])-48)   
    
    decalage = (jourmois-1) + 365*(annee-1)
    
    for i in range(0,moistotal-1):
            decalage+=mois[i]
    
    if (annee>2 or (moistotal>2 and annee==2)):
        decalage+=1
    
    return ((start+decalage) % 7)
    

print(jour("2012-03-01"))