# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 19:48:34 2015

@author: MAX
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 17:31:56 2015

@author: MAX
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
IGNORE = ["ele"]
IGNORE_PRE = ["gnis:", "is_in", "name:", "tiger", "sourc"]
city_mapping = {"DeWitt" : "Dewitt",
                "Fayetteville, NY" : "Fayetteville",
                "Mattdale" : "MattyDale",
                "east Syracuse" : "East Syracuse",
                "East Syracuse, NY" : "East Syracuse"}
                
def ignore_keys(key_value):
    if key_value in IGNORE:
        return True
    elif key_value[:5] in IGNORE_PRE:
        return True
    return False

def update_city(city, mapping):

    key_list = mapping.keys()
    if city in key_list:
        city = mapping['city']
    return city

def shape_element(element):
    node = {}

    if element.tag == "node" or element.tag == "way" :

      node['type'] = element.tag

       #Parse attributes
      for a in element.attrib:
        if a in CREATED:
          if 'created' not in node:
            node['created'] = {}
          node['created'][a] = element.attrib[a]

        elif a in ['lat', 'lon']:
          if 'pos' not in node:
            node['pos'] = [None, None]

          if a == 'lat':
            node['pos'][0] = float(element.attrib[a])
          else:
            node['pos'][1] = float(element.attrib[a])
        else:
          node[a] = element.attrib[a]

      #Iterate tag children to node or way
      for tag in element.iter("tag"):
        if not ignore_keys(tag.attrib['k']):
            if not problemchars.search(tag.attrib['k']):
              # Tags with single colon
              if lower_colon.search(tag.attrib['k']):
    
                # Single colon beginning with addr
                if tag.attrib['k'].find('addr') == 0:
                  #if len(tag.attrib['v']) > 25:
                    #pprint.pprint((tag.attrib['k'],tag.attrib['v']))
                  if 'address' not in node:
                    node['address'] = {}
    
                  sub_attr = tag.attrib['k'].split(':', 1)
    
                  try:
                    # clean postcode to first 5 
                    if sub_attr[1] == "postcode":
                        clean_zip = tag.attrib['v'][:5]
                        # skip zips found in audit.py that were wrong
                        if clean_zip == '13507' or clean_zip == '14224':
                            continue
                        else:
                            node['address'][sub_attr[1]] = clean_zip
                    elif sub_attr[1] == "city":
                        clean_city = update_city(tag.attrib['v'], city_mapping)
                        node['address'][sub_attr[1]] = clean_city
                    # all other addr: values
                    else:
                        node['address'][sub_attr[1]] = tag.attrib['v']
                    # exception for errors
                  except:
                    continue
    
    
                # All other single colons processed normally
                else:
                  node[tag.attrib['k']] = tag.attrib['v']

              # Tags with no colon
              elif tag.attrib['k'].find(':') == -1:
                node[tag.attrib['k']] = tag.attrib['v']

      # Iterate nd children
      for nd in element.iter("nd"):
        if 'node_refs' not in node:
          node['node_refs'] = []
        node['node_refs'].append(nd.attrib['ref'])

      return node
    else:
      return None   


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('C:\Users\MAX\Documents\Udacity\Data Analyst Nanodegree\Project3_Openstreetmap\syracuse_new-york.osm', False)
    #pprint.pprint(data)
    return data
#    correct_first_elem = {
#        "id": "261114295", 
#        "visible": "true", 
#        "type": "node", 
#        "pos": [41.9730791, -87.6866303], 
#        "created": {
#            "changeset": "11129782", 
#            "user": "bbmiller", 
#            "version": "7", 
#            "uid": "451048", 
#            "timestamp": "2012-03-28T18:31:23Z"
#        }
#    }
#    assert data[0] == correct_first_elem
#    assert data[-1]["address"] == {
#                                    "street": "West Lexington St.", 
#                                    "housenumber": "1412"
#                                      }
#    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
#                                    "2199822370", "2199822284", "2199822281"]

if __name__ == "__main__":
    data = test()
    
    
    
