#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 09:23:31 2020

@author: cassadygaier
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

confirmedDF = pd.read_csv("time_series_covid19_confirmed_US1.csv")
#print(confirmedDF)
deathDF = pd.read_csv("time_series_covid19_deaths_US2.csv")

confirmedData = confirmedDF.iloc[:,50:]
deathData = deathDF.iloc[:,51:]
#print(confirmedData)
#print(deathData)

fatalityRateList = []
deathNoList = []
for col in range(len(confirmedData.columns)):   
    confirmedNo = 0
    deathNo = 0
    
    for row in range(len(confirmedData.index)): 
        confirmedTemp = confirmedData.iloc[row,col]
        confirmedNo += confirmedTemp
        deathTemp = deathData.iloc[row,col]
        deathNo += deathTemp
    fatalityRate = deathNo / confirmedNo
    #print(fatalityRate)
    #print(confirmedNo)
    deathNoList = np.append(deathNoList, deathNo)
    fatalityRateList = np.append(fatalityRateList, fatalityRate)
    
tmpDict = {'date': confirmedData.columns,'death' : deathNoList,'fatality rate' : fatalityRateList } 

fatalityDF = pd.DataFrame(tmpDict)
print(fatalityDF) 
    
plt.suptitle('Fatality Rate in U.S.', fontsize = 20)
plt.xlabel('Time Frame Measured', fontsize = 15)
plt.ylabel('Fatality Rate', fontsize = 15)
plt.plot(confirmedDF.columns[50:],fatalityRateList, '-',color='blue')

plt.legend(['U.S.'],fontsize = 20)
plt.show()