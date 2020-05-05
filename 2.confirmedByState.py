# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:19:59 2020

@author: Cher
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

trainDF = pd.read_csv("time_series_covid19_confirmed_US.csv")
#print(trainDF)

#trainData = trainDF.iloc[:,50:]
#print(trainData.shape)
#print(len(trainData.columns))

stateList = ['Alabama', 'Alaska','Arizona','Arkansas','California','Colorado','Connecticut', 'Delaware', 'Florida', 'Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
#print(stateList)
#print(len(stateList))

for counter in range(len(stateList) -  1):
    trainData = trainDF[trainDF['Province_State'] == stateList[counter]].iloc[:,50:]
#    print(trainData)
    
    confirmedNoList = []
    for col in range(len(trainData.columns)):
#for col in range(75,77):    
        confirmedNo = 0
    
        for row in range(len(trainData.index)):
#    for row in range(0,5):    
            temp = trainData.iloc[row,col]
            confirmedNo += temp
        #print(temp)
    #print(confirmedNo)
        confirmedNoList = np.append(confirmedNoList, confirmedNo)
#print(confirmedNoList)
    tmpDict = {'state':stateList[counter],'date': trainData.columns,'confirmed number' : confirmedNoList} 

    confirmedDF = pd.DataFrame(tmpDict)
    print(confirmedDF) 

plt.suptitle('Covid-19 in the U.S.', fontsize = 20)
plt.xlabel('Date', fontsize = 15)
plt.ylabel('Total Confirmed Cases', fontsize = 15)
plt.plot(trainData.columns,confirmedNoList, '-',color='red', label='MSETrain')

plt.show()