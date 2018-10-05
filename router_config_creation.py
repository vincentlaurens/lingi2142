#!/usr/bin/env python3
import json
import os
import sys
import stat

# from pprint import pprint

from constants import PREFIXES, PATH, VLAN_USES

with open(PATH+'router_configuration.json') as data_file:
    data = json.load(data_file)
    

