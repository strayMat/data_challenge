# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:49:03 2016

@author: etienne
"""
import pandas as pd

def intervalle(X):
    i = 0
    a = ord(X[11])-48
    b = ord(X[12])-48
    c = ord(X[14])-48
    i+=a*2*10
    i+=b*2
    if c>0:
        i+=1
    return i

def centre(X):
    if(X=="CMS"): return 0
    if(X=="Crises"): return 1
    if(X=="Domicile"): return 2
    if(X=="Gestion"): return 3
    if(X=="Gestion - Accueil Telephonique"): return 4
    if(X=="Gestion Assurances"): return 5
    if(X=="Gestion Relation Clienteles"): return 6
    if(X=="Gestion Renault"): return 7
    if(X=="Japon"): return 8
    if(X=="Médical"): return 9
    if(X=="Nuit"): return 10
    if(X=="RENAULT"): return 11
    if(X=="Regulation Medicale"): return 12
    if(X=="SAP"): return 13
    if(X=="Services"): return 14
    if(X=="Tech. Axa"): return 15
    if(X=="Tech. Inter"): return 16
    if(X=="Téléphonie"): return 17
    return 18 #autre cas randoms si ça foire
    
