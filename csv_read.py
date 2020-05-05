#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 16:59:08 2020

@author: cassadygaier
"""

import csv

class csv_read:
    
    def __init__(self, fcsv):
        with open(fcsv) as f:
            self.data = []
            self.data_csv = csv.reader(f)
            for content in self.data_csv:
                self.data.append(content)
        
    # return data for cases&time graph
    def cases_time(self):
        cases = []
        time = []
        i = 0
        for content in self.data:
            if i == 0:
                i += 1
                continue
            cases.append(int(content[2]))
            time.append(content[0][4:-2]+'.'+content[0][-2:])
            i += 1
        cases.reverse()
        time.reverse()

        return cases, time
    
    # return data for grpah death map
    def states_death(self):
        line = 0
        death_state = {}
        for content in self.data:
            if line == 0:
                line +=1
                continue
            area_death = int(content[-1])
            if content[6] in death_state:
                death_state[content[6]] += area_death
            else:
                death_state[content[6]] = 0
        list_state = []
        for key, value in death_state.items():
            list_state.append([key, value])
        list_state.sort(key = lambda x : x[1], reverse = False)
        return list_state

    # return data for graph death&cured
    def reco_death(self):
        death, cured, time = [], [], []
        i = 0
        for content in self.data:
            if not i:
               i += 1
               continue
            if not content[14] and not content[11]:
               continue
            if not content[14]:
                death.append(0)
            else:
                death.append(int(content[14]))
            if not content[11]:
                cured.append(0)
            else:
                cured.append(int(content[11]))
            time.append(content[0][4:-2]+'.'+content[0][-2:])
            
        death.reverse()
        cured.reverse()
        time.reverse()
        
        return death, cured, time