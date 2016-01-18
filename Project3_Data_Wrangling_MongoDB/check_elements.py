# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:37:46 2015

@author: MAX
"""
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

def check_elements(file_in):
    attrib_set = set()   
    for _, element in ET.iterparse(file_in):
      for a in element.attrib:
          attrib_set.add(a)
    
    return attrib_set
        

def test():

    data = check_elements('C:\Users\MAX\Documents\Udacity\Data Analyst Nanodegree\Project3_Openstreetmap\syracuse_new-york.osm')
    pprint.pprint(data)


if __name__ == "__main__":
    test()