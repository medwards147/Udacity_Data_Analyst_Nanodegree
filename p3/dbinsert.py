# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 19:04:08 2015

@author: MAX
"""

from pymongo import MongoClient

#client = MongoClient("mongodb://localhost:27017")
#db = client.project
#collection = db.syracuse


#with open(syracuse) as f:
#
#    collection = db.syracuse
#    collection.insert(syracuse)


def insert_data(data):
    client = MongoClient("mongodb://localhost:27017")    
    db = client.project
    db.project.insert(data)

if __name__ == "__main__":
    
    from pymongo import MongoClient
    #client = MongoClient("mongodb://localhost:27017")
    
    data = []
    syracuse = 'C:\Users\MAX\Documents\Udacity\Data Analyst Nanodegree\Project3_Openstreetmap\syracuse_new-york.json'
    with open(syracuse) as f:
        #data = json.loads(f.read())
        for line in f:
            data.append(json.loads(line))
    insert_data(data)
