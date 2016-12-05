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
    if(X=="CAT"): return 18
    if(X=="CMS"): return 0
    if(X=="Crises"): return 1
    if(X=="Domicile"): return 2
    if(X=="Evenements"): return 19
    if(X=="Gestion"): return 3
    if(X=="Gestion Amex"): return 20
    if(X=="Gestion Clients"): return 21
    if(X=="Gestion DZ"): return 22
    if(X=="Gestion - Accueil Telephonique"): return 4
    if(X=="Gestion Assurances"): return 5
    if(X=="Gestion Relation Clienteles"): return 6
    if(X=="Gestion Renault"): return 7
    if(X=="Japon"): return 8
    if(X=="Manager"): return 23
    if(X=="Mécanicien"): return 24
    if(X=="Médical"): return 9
    if(X=="Nuit"): return 10
    if(X=="RENAULT"): return 11
    if(X=="Prestataires"): return 25
    if(X=="RTC"): return 26
    if(X=="Regulation Medicale"): return 12
    if(X=="SAP"): return 13
    if(X=="Services"): return 14
    if(X=="Tech. Axa"): return 15
    if(X=="Tech. Inter"): return 16
    if(X=="Tech. Total"): return 27
    if(X=="Téléphonie"): return 17
    return -1 #autre cas randoms si ça foire

def holidays(X):
    x = X.split('-')
    year = int(x[0])
    month = int(x[1])
    day = int(x[2])

    holidays = 0
    if year==2011:
        if month==1:
            if day<=2:
                holidays+=3
        if month==2:
            if day>=12: 
                holidays+=1
            if day>=19: 
                holidays+=1
            if day>=26: 
                holidays+=1
            if day>=28: 
                holidays-=1
        if month==3:
            if day<=14: 
                holidays+=1
            if day<=7:  
                holidays+=1
        if month==4:
            if day>=9:  
                holidays+=1
            if day>=16: 
                holidays+=1
            if day>=23: 
                holidays+=1
            if day>=26: 
                holidays-=1
        if month==5:
            if day<=9:  
                holidays+=1
            if day<=2:  
                holidays+=1
        if month==10:
            if day>=27: 
                holidays+=3
        if month==11:
            if day<=7:  
                holidays+=3
        if month==12:
            if day>=17: 
                holidays+=3
    if year==2012:
        if month==1:
            if day<=2:
                holidays+=3
        if month==2:
            if day>=11: 
                holidays+=1
            if day>=18: 
                holidays+=1
            if day>=25: 
                holidays+=1
            if day<=27: 
                holidays-=1
        if month==3:
            if day<=12: 
                holidays+=1
            if day<=5:  
                holidays+=1
        if month==4:
            if day>=7:  
                holidays+=1
            if day>=14: 
                holidays+=1
            if day>=21: 
                holidays+=1
            if day>=24: 
                holidays-=1
            if day>=30: 
                holidays-=1
        if month==5:
            if day<=7:  
                holidays+=1
        if month==10:
            if day>=27: 
                holidays+=3
        if month==11:
            if day<=7:  
                holidays+=3
        if month==12:
            if day>=22: 
                holidays+=3
    if year==2013:
        if month==1:
            if day<=6:
                holidays+=3
        if month==2:
            if day>=16: 
                holidays+=1
            if day>=23: 
                holidays+=1
        if month==3:
            if day<=18:
                holidays+=1
            if day<=11: 
                holidays+=1
            if day<=4: 
                holidays+=1
            if day<2:   
                holidays-=1
        if month==4:
            if day>=13: 
                holidays+=1
            if day>=20: 
                holidays+=1
            if day>=27: 
                holidays+=1
            if day>=29: 
                holidays-=1
        if month==5:
            if day<=5:  
                holidays+=1
            if day<=12: 
                holidays+=1
        if month==10:
            if day>=19: 
                holidays+=3
        if month==11:
            if day<=3:  
                holidays+=3
        if month==12:
            if day>=21: 
                holidays+=3
            
        if month==7 or month==8:  
            holidays+=3

    return holidays
