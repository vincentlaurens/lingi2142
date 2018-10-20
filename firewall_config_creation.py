#group3 : firewall_config_creation.py - Python 3 - Read a parsed file (json)

import json
import os
import sys

from pprint import pprint
from constants import PATH

#pprint(data)
pprint("Writting:"+PATH+"iptables/launchfirewall.sh")


####################launchfirewall.sh###############################"
iptables_file = open(PATH+"iptables/launchfirewall.sh", "w")
iptables_file.write("#!/bin/bash\n\n"
	"echo \"Starting the firewalls on all routers ...\"\n\n"

	"sudo ip netns exec \"Halles\" ./Halles.sh\n\n"

	"sudo ip netns exec \"Pyth\" ./Pyth.sh\n\n"

	"sudo ip netns exec \"Stev\" ./Stev.sh\n\n"

	"sudo ip netns exec \"SH1C\" ./SH1C.sh\n\n"

	"sudo ip netns exec \"Carno\" ./Carno.sh\n\n"

	"sudo ip netns exec \"Mich\" ./Mich.sh\n\n"

	"echo \"All the firewalls have been set !\"\n\n"

	"exit 0")
iptables_file.close()
os.chmod(PATH+"iptables/launchfirewall.sh", 0o766)
	##########

####################routerfirewall.sh###############################"
with open(PATH+'firewall_configuration_file.json') as data_file:
	data = json.load(data_file)


for router, configs_firewall in data.items():
	pprint(router)
	router_firewall_config_file = open(PATH+"iptables/"+router+".sh", "w")

	router_firewall_config_file.write("#!/bin/bash\n"
						"#Document generates by script firewall_config_creation.py, have a look on this python script for more details\n\n\n"

						"# Flush all rules and delete all chains\n"
						"# because it is best to startup cleanly\n"
						"ip6tables -F\n"
						"ip6tables -X\n"
						"ip6tables -t nat -F\n"
						"ip6tables -t nat -X\n"
						"ip6tables -t mangle -F \n"
						"ip6tables-t mangle -X \n"
						"ip6tables -L\n\n"
						"#all to Zero\n"
						"ip6tables -Z\n"
						"ip6tables -t nat -Z\n"
						"ip6tables -t mangle -Z\n"
						"ip6tables -t filter -D INPUT -s 2001:db8::/32 -j DROP\n"
						"ip6tables -t filter -D INPUT -s 2001:db8::/32 -j DROP\n"
						"ip6tables -P INPUT DROP\n"
						"ip6tables -P FORWARD DROP\n"
						"ip6tables -P OUTPUT ACCEPT\n\n"
						"# Required for the loopback interface\n"
						"ip6tables -A INPUT -i lo -j ACCEPT\n"
						"ip6tables -A OUTPUT -o lo -j ACCEPT\n\n"
						"# Reject connection attempts not initiated from the host\n"
						"ip6tables -A INPUT -p tcp --syn -j DROP\n\n"
						"# Allow return connections initiated from the host\n"
						"ip6tables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT\n"
						"ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
						"ip6tables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
						"ip6tables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT\n\n"
						"#Authorize important ICMP Packet\n"
						"ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -j ACCEPT\n"
						"ip6tables-A INPUT -p icmpv6 --icmpv6-type time-exceeded -j ACCEPT\n"
						"ip6tables -A INPUT -p icmpv6 --icmpv6-type destination-unreachable -j ACCEPT\n"
						"ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -m limit --limit 50/min -j ACCEPT\n"
						"ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-reply -m limit --limit 50/min -j ACCEPT\n"
						"ip6tables -A OUTPUT -p icmpv6 -m limit --limit 5/second  -j ACCEPT\n\n"
						"# Allow logging in via SSH\n"
						"ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT\n\n"
						"# Restrict incoming SSH to a specific network interface\n"
						)
	for rules in configs_firewall["conf_firewall"]:
		router_firewall_config_file.write(rules+"\n")
	router_firewall_config_file.write(
						"\n"
						"# Allow external access to your HTTP server\n"
						"ip6tables -A INPUT -p tcp -m multiport --dport 80,443,8080 -j ACCEPT\n\n"
						"# Allow external access to your unencrypted mail server, SMTP,IMAP, and POP3.\n"
						"ip6tables -A INPUT -p tcp -m multiport --dport 25,110,143 -j ACCEPT\n"
						)
	router_firewall_config_file.close()
	os.chmod(PATH+"iptables/"+router+".sh", 0o766)
	##########
