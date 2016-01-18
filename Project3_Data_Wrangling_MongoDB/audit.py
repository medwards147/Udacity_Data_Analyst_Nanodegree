# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 17:34:27 2015

@author: MAX
"""

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = 'C:\Users\MAX\Documents\Udacity\Data Analyst Nanodegree\Project3_Openstreetmap\syracuse_new-york.osm'
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

expected_zips = ['13201', '13205', '13209', '13214', '13219', '13225', '13251', '13202',
                 '13206', '13210', '13215', '13220', '13235', '13252', '13203', '13207', '13211',
                 '13217', '13221', '13244', '13261', '13204', '13208', '13212', '13218', '13224',
                 '13250', '13290', '13022', '13027', '13031', '13039', '13041', '13057', '13066',
                 '13078', '13088', '13090', '13104', '13108', '13116', '13120', '13152', '13164',
                 '13198']

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road" }
# Used this in data.py to clean
#city_mapping = {"DeWitt" : "Dewitt",
#                "Fayetteville, NY" : "Fayetteville",
#                "Mattdale" : "MattyDale",
#                "east Syracuse" : "East Syracuse",
#                "East Syracuse, NY" : "East Syracuse"}


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_postalcode(postalcode):
    
    if postalcode > 5:
        five_zip = postalcode[:5]
    else:
        five_zip = postalcode
    
    if five_zip not in expected_zips:
        return five_zip

def audit_city(city_val):
 
    return city_val
    
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postal(elem):
    return (elem.attrib['k'] == "addr:postcode")
    
def is_city(elem):
    return (elem.attrib['k'] == "addr:city")

# audits street, zip, city
def audit(osmfile, audit_value = ''):
    osm_file = open(osmfile, "r")
    if audit_value == 'postal':
        zip_fixed= set()
        for event, elem in ET.iterparse(osm_file, events=("start",)):
    
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if is_postal(tag):
                        zip_fixed.add(audit_postalcode(tag.attrib['v']))
        return zip_fixed

    elif audit_value == 'city':
        city_fixed = set()
        for event, elem in ET.iterparse(osm_file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if is_city(tag):
                        city_fixed.add(audit_city(tag.attrib['v']))
        return city_fixed                        
    
    else:
        street_types = defaultdict(set)
        for event, elem in ET.iterparse(osm_file, events=("start",)):

            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if is_street_name(tag):
                        audit_street_type(street_types, tag.attrib['v'])

        return street_types
    


def update_name(name, mapping):

    m = street_type_re.search(name)
    if m:
        result = m.group()
        if result not in expected:
            # re.sub(pattern, repl, string, count=0, flags=0)
            name = re.sub(street_type_re, mapping[result], name) 
    return name

# USED THIS IN data.py
#def update_city(city, mapping):
#
#    key_list = mapping.keys()
#    if city in key_list:
#        city = mapping['city']
#    return city


def test():
    st_types = audit(OSMFILE, 'city')
    pprint.pprint(st_types)

   # print st_types


if __name__ == '__main__':
    test()