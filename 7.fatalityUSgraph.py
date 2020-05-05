# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 20:23:13 2020

@author: Cher
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

confirmedDF = pd.read_csv("time_series_covid19_confirmed_US.csv")
#print(confirmedDF)
deathDF = pd.read_csv("time_series_covid19_deaths_US.csv")

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
    
plt.suptitle('fatality rate in U.S.', fontsize = 20)
plt.xlabel('Date', fontsize = 15)
plt.ylabel('Fatality Rate', fontsize = 15)
plt.plot(confirmedDF.columns[50:],fatalityRateList, '-',color='blue')

plt.legend(['U.S.'],fontsize = 25)
plt.show()