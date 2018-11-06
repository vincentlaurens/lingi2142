#group3 : router_config_creation.py - Python 3 - Read a parsed file (json)

import json
import os
import sys
import string

from pprint import pprint
from constants import PATH, PREFIXES_ADDRESS, VLAN_USES

with open(PATH+'router_configuration_file.json') as data_file:
	data = json.load(data_file)



pprint("Writting router_config:")
#read json items by items which are routers
for router, configs in data.items():

	###########################"Write _boot file config"##################
	router_boot_file = open(PATH+"group3_cfg/"+router+"_boot.sh", "w")
	router_boot_file.write("#!/bin/bash\n\n"
	                        "sysctl -p \n"
						    #"./iptables/"+router+".sh \n"
                           )
	router_boot_file.close()
	os.chmod(PATH+"group3_cfg/"+router+"_boot.sh", 0o766)
	##########
	########################"Write _start file Config"###################################
	router_start_file = open(PATH+"group3_cfg/"+router+"_start.sh", "w")
	router_start_file.write("#!/bin/bash \n\n"
	                        "# This file has been generated automatically, see router_config_creation.py \n"
                            )

	##############isp interfaces on routers ########################################
	if configs["setup_bgp_conf"] == "true":
		for isp, isp_configs in configs["isp"].items():
			router_start_file.write("ip link set dev "+isp+" up \n"
			                        "ip address add dev "+isp+" "+isp_configs["self_address"]+"  \n\n"
                                    )
	##############eth interfaces on routers ########################################
	for eth, eth_configs in configs["eths"].items():
		site = eth_configs
		for prefix_address in PREFIXES_ADDRESS:
			router_start_file.write("ip address add dev "+router+"-"+eth+" "+prefix_address+configs["City"]+site+"::"+configs["router_id"]+"/64 \n")

	router_start_file.write("\n")

	##############lans interfaces on routers ########################################
	if "lans" in configs:
		for lan, lan_configs in configs["lans"].items():
			for prefix_address in PREFIXES_ADDRESS:
				router_start_file.write("ip address add dev "+router+"-"+lan+" "+prefix_address+configs["City"]+configs["lan_interface"]+lan_configs+"::"+configs["router_id"]+"/64 \n")
	router_start_file.write("\n")

	##############vlan interfaces #######################################################
	if "vlans" in configs:
		for vlan, location in configs["vlans"].items():
			for vlan_use in VLAN_USES:
				router_start_file.write("ip link add link "+router+"-"+vlan+" name "+router+"-"+vlan+"."+vlan_use+location+" type vlan id 0x"+vlan_use+location+" \n")
				router_start_file.write("ip link set dev "+router+"-"+vlan+"."+vlan_use+location+" up \n")
				for prefix in PREFIXES_ADDRESS:
					router_start_file.write("ip address add dev "+router+"-"+vlan+"."+vlan_use+location+" "+prefix+vlan_use+location+"::/64 \n")
			router_start_file.write("\n")
	########################"Prefix management rules"###################################
	if "lb_commands" in configs:
		for command in configs["lb_commands"]:
			router_start_file.write(command+"\n")

	router_start_file.write("\n")
	router_start_file.write("bird6 -s /tmp/"+router+"_bird.ctl -P /tmp/"+router+"_bird.pid \n")
	router_start_file.close()
	os.chmod(PATH+"group3_cfg/"+router+"_start.sh", 0o766)
	###########
	#####################"Write Sysctl File"##########################################
	router_sysctl_config = open(PATH+"group3_cfg/"+router+"/sysctl.conf", "w")
	router_sysctl_config.write("net.ipv6.conf.all.disable_ipv6=0\n"
	                            "net.ipv6.conf.all.forwarding=1\n"
	                            "net.ipv6.conf.default.disable_ipv6=0\n"
	                            "net.ipv6.conf.default.forwarding=1\n"
                                )
	router_sysctl_config.close()
	###########
	##################"Write bird Config"########################

	router_bird_file = open(PATH+"group3_cfg/"+router+"/bird/bird6.conf", "w")
	router_bird_file.write("# group3: Bird6 File config "+router+".\n\n"

	                        "router id 0.0.0."+configs["router_id"]+";\n\n"

	                        "log \"/etc/log/bird_log\" all; \n"
	                        "debug protocols all;  \n\n"
                           )

	if configs["setup_bgp_conf"] == "true":
		router_bird_file.write("filter import_ospf_filter\n"
		                        " { \n"

                                "	if net = ::/0 then accept;\n\n"
                                "	if net ~ fd00:200:3::/48 then accept;\n"
		                        "	if net ~ fd00:300:3::/48 then accept;\n"
		                        "else reject;\n"
		                        "}"

		                        "filter export_ospf_filter\n"
                                " { \n"
                                "	if net = ::/0 then accept;\n\n"
                                "	if proto = \"static_bpg\" then reject;\n"

                                "	if net = fd00:200:3::/48 then reject;\n"
		                        "	if net = fd00:300:3::/48 then reject;\n"

		                        "	if net ~ fd00:200:3::/48 then accept;\n"
		                        "	if net ~ fd00:300:3::/48 then accept;\n"
		                        "else reject;\n"
		                        "}\n\n"
                                )
	else:
		router_bird_file.write("filter import_ospf_filter\n"
		                        " { \n"

                                "	if net = ::/0 then accept;\n\n"
                                "	if net ~ fd00:200:3::/48 then accept;\n"
                                "	if net ~ fd00:300:3::/48 then accept;\n"
                                "else reject;\n"
                                "}\n\n"

                                "filter export_ospf_filter\n"
                                " { \n"
                                "	if net = ::/0 then accept;\n\n"
                                "	if net ~ fd00:200:3::/48 then accept;\n"
                                "	if net ~ fd00:300:3::/48 then accept;\n"
                                "else reject;\n"
                                "}\n\n"
                               )

	router_bird_file.write("protocol kernel {\n"
                            "        learn;\n"
                            "        scan time 20;\n"
                            "        import all;\n"
                            "        export all;\n"
                            "}\n\n"

                            "protocol device { \n"
                            "        scan time 10;\n"
                            "}\n\n"
                           )

	if configs["setup_bgp_conf"] == "true":
		#############conf bgp
		router_bird_file.write("protocol static static_bgp {\n"
		                        "        import all;\n\n"
		                        "        route fd00:200:3::/48 reject ;\n"
		                        "        route fd00:300:3::/48 reject ;\n"
                                "}\n\n"
                               )


		for bgp, bgp_configs in configs["isp"].items():
			router_bird_file.write("protocol bgp provider"+bgp_configs["name_bgp"]+"{ \n"
                                   "    local as "+bgp_configs["asn"]+";\n"
                                   "    neighbor "+bgp_configs["neighbor_address"]+" as "+bgp_configs["name_bgp"]+";\n"
                                   "    import where net = ::/0;\n"
                                   "    export where proto = \"static_bgp\";  \n"
                                    "}\n\n"
                                    )

	router_bird_file.write("protocol ospf {\n"
                            "        export filter export_ospf_filter;\n"
                            "        import filter import_ospf_filter;\n"
                        
                            "        area 0.0.0.0{\n"
                            "                interface \"*eth*\" {\n"
                            "                        hello 1;\n"
                            "                        dead 3;\n"
                            "                };\n"
                            "                interface \"*lan*\" {\n"
                            "                        stub 1;\n"
                            "                };\n"
                            "                interface \"*lo*\" {\n"
                            "                        stub 1;\n"
                            "                };\n"
                            "        };\n"
                            "}\n\n"
                           )


	router_bird_file.close()





