#!/usr/bin/env python3
import json
import os
import sys
import stat

# from pprint import pprint

from constants import PREFIXES, PATH, VLAN_USES

with open(PATH+'router_configuration.json') as data_file:
    data = json.load(data_file)
    
  ######################## #################router_start config ################################################

    router_start_config = open(PATH+"project_cfg/"+router+"_start", "w")
    router_start_config.write("#!/bin/bash \n\n")
    router_start_config.write("# This file has been generated automatically, see router_config_creation.py for details. \n\n")

    

