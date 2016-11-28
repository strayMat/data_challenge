# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:49:03 2016
@author: etienne
"""
#import pandas as pd

#def assignementNumber(X):
#    col_names = pd.read_csv("field_description.csv", sep = ",")['Colonne']

def intervalle(X):
   x = str(X).split()[1].split(':')
   return int(x[0])*2 + (int(x[1])==30)
   
   
def centre(X):
    if(X=="CAT"): return 0
    if(X=="CMS"): return 1
    if(X=="Crises"): return 2
    if(X=="Domicile"): return 3
    if(X=="Evenements"): return 4
    if(X=="Gestion"): return 5
    if(X=="Gestion Amex"): return 6
    if(X=="Gestion Clients"): return 7
    if(X=="Gestion DZ"): return 8
    if(X=="Gestion - Accueil Telephonique"): return 9
    if(X=="Gestion Assurances"): return 10
    if(X=="Gestion Relation Clienteles"): return 11
    if(X=="Gestion Renault"): return 12
    if(X=="Japon"): return 13
    if(X=="Manager"): return 14
    if(X=="Mécanicien"): return 15
    if(X=="Médical"): return 16
    if(X=="Nuit"): return 17
    if(X=="RENAULT"): return 18
    if(X=="Prestataires"): return 19
    if(X=="RTC"): return 20
    if(X=="Regulation Medicale"): return 21
    if(X=="SAP"): return 22
    if(X=="Services"): return 23
    if(X=="Tech. Axa"): return 24
    if(X=="Tech. Inter"): return 25
    if(X=="Tech. Total"): return 26
    if(X=="Téléphonie"): return 27
    return 18 #autre cas randoms si ça foire

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