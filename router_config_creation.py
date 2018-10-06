#router_config.py - Python 3 - Read a parsed file (json)

import json
from pprint import pprint
from constants import PATH


with open(PATH+'router_configuration_file.json') as data_file:    
    data = json.load(data_file)

pprint(data)

#Write the json content on an other file.
