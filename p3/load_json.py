# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 20:34:25 2015

@author: MAX
"""

import json

data = []
with open('C:\Users\MAX\Documents\Udacity\Data Analyst Nanodegree\Project3_Openstreetmap\syracuse_new-york.json') as f:
    for line in f:
        data.append(json.loads(line))