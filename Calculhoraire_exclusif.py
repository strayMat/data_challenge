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
    if(X=="CAT"): return 0
    if(X=="CMS"): return 1
    if(X=="Crises"): return 2
    if(X=="Domicile"): return 3
    if(X=="Evenements"): return 4
    if(X=="Gestion"): return 5
    if(X=="Gestion - Accueil Telephonique"): return 6
    if(X=="Gestion Amex"): return 7
    if(X=="Gestion Assurances"): return 8
    if(X=="Gestion Clients"): return 9
    if(X=="Gestion DZ"): return 10
    if(X=="Gestion Relation Clienteles"): return 11
    if(X=="Gestion Renault"): return 12
    if(X=="Japon"): return 13
    if(X=="Manager"): return 14
    if(X=="Mécanicien"): return 15
    if(X=="Médical"): return 16
    if(X=="Nuit"): return 17
    if(X=="Prestataires"): return 18
    if(X=="Regulation Medicale"): return 19
    if(X=="RENAULT"): return 20
    if(X=="RTC"): return 21
    if(X=="SAP"): return 22    
    if(X=="Services"): return 23
    if(X=="Tech. Axa"): return 24
    if(X=="Tech. Inter"): return 25
    if(X=="Tech. Total"): return 26
    if(X=="Téléphonie"): return 27
    
    return -1 #autre cas randoms si ça foire

def inverse(X):
    if(X==0): return "CAT"
    if(X==1): return "CMS"
    if(X==2): return "Crises"
    if(X==3): return "Domicile"
    if(X==4): return "Evenements"
    if(X==5): return "Gestion"
    if(X==6): return "Gestion - Accueil Telephonique"
    if(X==7): return "Gestion Amex"
    if(X==8): return "Gestion Assurances"
    if(X==9): return "Gestion Clients"
    if(X==10): return "Gestion DZ"
    if(X==11): return "Gestion Relation Clienteles"
    if(X==12): return "Gestion Renault"
    if(X==13): return "Japon"
    if(X==14): return "Manager"
    if(X==15): return "Mécanicien"
    if(X==16): return "Médical"
    if(X==17): return "Nuit"
    if(X==18): return "Prestataires"
    if(X==19): return "Regulation Medicale"
    if(X==20): return "RENAULT"
    if(X==21): return "RTC"
    if(X==22): return "SAP"
    if(X==23): return "Services"
    if(X==24): return "Tech. Axa"
    if(X==25): return "Tech. Inter"
    if(X==26): return "Tech. Total"
    if(X==27): return "Téléphonie"
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
