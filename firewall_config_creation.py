#group3 : firewall_config_creation.py - Python 3 - Read a parsed file (json)

import json
import os
import sys

from pprint import pprint
from constants import PATH, PREFIXES_ADDRESS

#pprint(data)
pprint("Writting:")

####################launchfirewall.sh###############################"
iptables_file = open(PATH+"iptables/launchfirewall.sh", "w")
	iptables_file.write("#!/bin/bash\n\n"
	"echo "Starting the firewalls on all routers ..."\n\n"

	"sudo ip netns exec "Halles" ./Halles.sh\n\n"

	"sudo ip netns exec "Pyth" ./Pyth.sh\n\n"

	"sudo ip netns exec "Stev" ./Stev.sh\n\n"

	"sudo ip netns exec "SH1C" ./SH1C.sh\n\n"

	"sudo ip netns exec "Carno" ./Carno.sh\n\n"

	"sudo ip netns exec "Mich" ./Mich.sh\n\n"

	"echo "All the firewalls have been set !"\n\n"

	"exit 0\n\n")
	router_boot_file.close()
	##########

####################routerfirewall.sh###############################"
router_boot_file = open(PATH+"iptables/"+router+".sh", "w")
	router_boot_file.write("#!/bin/bash\n\n")
	router_boot_file.close()
	##########
