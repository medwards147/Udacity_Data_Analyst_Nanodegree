# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 17:33:31 2015

@author: MAX
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    # YOUR CODE HERE
    tags = {}

    tree = ET.iterparse(filename)
    
    for event, elem in tree:
        if elem.tag in tags:
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1       


    return tags

def test():

    tags = count_tags('C:\Users\MAX\Documents\Udacity\Data Analyst Nanodegree\Project3_Openstreetmap\syracuse_new-york.osm')
    pprint.pprint(tags)

    

if __name__ == "__main__":
    test()