# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:49:03 2016
@author: etienne
"""
#import pandas as pd

#def assignementNumber(X):
#    col_names = pd.read_csv("field_description.csv", sep = ",")['Colonne']

def intervalle(X):
   x = str(X).split(' ')[1].split(':')
   return int(x[0])*2 + (int(x[1])==30)
   
   
def centre(X):
    #if(X=="CAT"): return 0
    if(X=="CMS"): return 0
    if(X=="Crises"): return 1
    if(X=="Domicile"): return 2
    #if(X=="Evenements"): return 3
    if(X=="Gestion"): return 3
    #if(X=="Gestion Amex"): return 6
    #if(X=="Gestion Clients"): return 7
    #if(X=="Gestion DZ"): return 8
    if(X=="Gestion - Accueil Telephonique"): return 4
    if(X=="Gestion Assurances"): return 5
    if(X=="Gestion Relation Clienteles"): return 6
    if(X=="Gestion Renault"): return 7
    if(X=="Japon"): return 8
    #if(X=="Manager"): return 14
    #if(X=="Mécanicien"): return 15
    if(X=="Médical"): return 9
    if(X=="Nuit"): return 10
    if(X=="RENAULT"): return 11
    #if(X=="Prestataires"): return 19
    #if(X=="RTC"): return 20
    if(X=="Regulation Medicale"): return 12
    if(X=="SAP"): return 13
    if(X=="Services"): return 14
    if(X=="Tech. Axa"): return 15
    if(X=="Tech. Inter"): return 16
    #if(X=="Tech. Total"): return 26
    if(X=="Téléphonie"): return 17
    return -1 #autre cas randoms si ça foire
