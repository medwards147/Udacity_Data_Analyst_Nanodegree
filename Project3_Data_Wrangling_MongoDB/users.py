# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 17:34:09 2015

@author: MAX
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return


def process_map(filename):
    users = set()
    for event, element in ET.iterparse(filename):
        if 'user' in element.attrib:
            users.add(element.attrib['user'])
        else:
            continue

    return users


def test():

    users = process_map('C:\Users\MAX\Documents\Udacity\Data Analyst Nanodegree\Project3_Openstreetmap\syracuse_new-york.osm')
    pprint.pprint(users)
    #assert len(users) == 6



if __name__ == "__main__":
    test()