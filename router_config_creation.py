#group3 : router_config_creation.py - Python 3 - Read a parsed file (json)

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

	###########################"Write _boot file config"##################
	router_boot_file = open(PATH+"group3_cfg/"+router+"_boot.sh", "w")
	router_boot_file.write("#!/bin/bash\n\n")
	router_boot_file.write("sysctl -p")
	router_boot_file.close()
	##########
	######"""##################"Write _start file Config"###################################
	router_start_file = open(PATH+"group3_cfg/"+router+"_start.sh", "w")
	router_start_file.write("#!/bin/bash \n\n")
	router_start_file.write("# This file has been generated automatically, see router_config_creation.py for details. \n\n")
	

	for isp, isp_configs in configs["isp"].items():
		router_start_file.write("ip link set dev "+isp+" up \n")
		router_start_file.write("ip address add dev "+isp+" "+isp_configs["self_address"]+"  \n")

	router_start_file.write("\n")
	router_start_file.write("bird6 -s /tmp/"+router+".ctl -P /tmp/"+router+"_bird.pid \n")
	#router_start_filewrite("radvd -p /var/run/radvd/"+router+"_radvd.pid -C /etc/radvd/"+router+".conf -m logfile -l /var/log/radvd/"+router+".log\n")

	router_start_file.close()
	os.chmod(PATH+"group3_cfg/"+router+"_start.sh", 0o766)
	###########
	#####################"Write Sysctl File"##########################################
	router_sysctl_config = open(PATH+"group3_cfg/"+router+"/sysctl.conf", "w")
	router_sysctl_config.write("net.ipv6.conf.all.disable_ipv6=0\n")
	router_sysctl_config.write("net.ipv6.conf.all.forwarding=1\n")
	router_sysctl_config.write("net.ipv6.conf.default.disable_ipv6=0\n")
	router_sysctl_config.write("net.ipv6.conf.default.forwarding=1\n")
	router_sysctl_config.close()
	###########
	##################"Write bird Config"########################

	router_bird_file = open(PATH+"group3_cfg/"+router+"/bird/bird6.conf", "w")
	router_bird_file.write("# group3: Bird6 File config "+router+".\n\n")

	router_bird_file.write("router id 3.0.0."+configs["router_id"]+";\n\n")

	router_bird_file.write("log ""/etc/log/bird_log"" all; \n")
	router_bird_file.write("debug protocols all;  \n\n")

	router_bird_file.write("protocol kernel {\n")
	router_bird_file.write("	learn;\n")
	router_bird_file.write("	scan time 20\n")
	router_bird_file.write("	export all;\n")
	router_bird_file.write("}\n\n")

	router_bird_file.write("protocol device { \n")
	router_bird_file.write("	scan time 10;\n")
	router_bird_file.write("}\n\n")

	router_bird_file.write("protocol static static_ospf {\n")
	router_bird_file.write("	import all;\n\n")
	for isp, isp_configs in configs["isp"].items():
		router_bird_file.write("	route ::/0 via "+isp_configs["neighbor_address"]+";\n")
		router_bird_file.write("}\n\n")

	router_bird_file.write("protocol ospf {\n")
	router_bird_file.write("	import all;\n")
	router_bird_file.write("	export where proto = ""static_ospf"";\n")
	router_bird_file.write("	area 0.0.0.0{\n")
	router_bird_file.write("		interface ""*eth*"" {\n")
	router_bird_file.write("			hello 1;\n")
	router_bird_file.write("			dead 3;\n")
	router_bird_file.write("		};\n")
	router_bird_file.write("		interface ""*lan*"" {\n")
	router_bird_file.write("			stub 1;\n")            	
	router_bird_file.write("		};\n")
	router_bird_file.write("		interface ""*lo*"" {\n")
	router_bird_file.write("			stub 1;\n")            	
	router_bird_file.write("		};\n")
	router_bird_file.write("	};\n")
	router_bird_file.write("}\n\n")
	#for ospf, ospf_configs in configs["ospf"].items():


	for bgp, bgp_configs in configs["isp"].items():
		router_bird_file.write("protocol bgp provider"+bgp_configs["name_bgp"]+"{ \n")
		router_bird_file.write("	local as "+bgp_configs["asn"]+";\n")
		router_bird_file.write("	neighbor "+bgp_configs["neighbor_address"]+" as "+bgp_configs["name_bgp"]+";\n")
		router_bird_file.write("	export all;  \n")
		router_bird_file.write("	import all;  \n")
		router_bird_file.write("}\n")

	router_bird_file.close()
	##############
