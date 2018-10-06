#router_config.py - Python 3 - Read a parsed file (json)

import json
import os
import sys

from pprint import pprint
from constants import PATH


with open(PATH+'router_configuration_file.json') as data_file:    
    data = json.load(data_file)

#pprint(data)
pprint("Writting:")
#read json items by items which are routers
for router, configs in data.items():
	#os.chmod(PATH+"group3_cfg/"+router+"_start", 0o666)
	writein_file = open(PATH+"group3_cfg/"+router+"_start", "w")
	writein_file.write("#!/bin/bash \n\n")
	writein_file.write("# This file has been generated automatically, see router_config_creation.py for details. \n\n")
	

	for isp, isp_configs in configs["isp"].items():
		writein_file.write("ip link set dev "+isp+" up \n")
		writein_file.write("ip address add dev "+isp+" "+isp_configs["self_address"]+"  \n")

	writein_file.write("\n")
	writein_file.write("bird6 -s /tmp/"+router+".ctl -P /tmp/"+router+"_bird.pid \n")
	writein_file.write("radvd -p /var/run/radvd/"+router+"_radvd.pid -C /etc/radvd/"+router+".conf -m logfile -l /var/log/radvd/"+router+".log\n")

	writein_file.close()





