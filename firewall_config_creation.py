#group3 : firewall_config_creation.py - Python 3 - Read a parsed file (json)

import json
import os
import sys

from pprint import pprint
from constants import PATH

#pprint(data)
#pprint("Writting:"+PATH+"iptables/launchfirewall.sh")


####################launchfirewall.sh###############################"
iptables_file = open(PATH+"iptables/launchfirewall.sh", "w")
iptables_file.write("#!/bin/bash\n\n"
	"echo \"Starting the firewalls on all routers ...\"\n\n"

	"sudo ip netns exec \"Halles\" ./iptables/Halles.sh\n\n"

	"sudo ip netns exec \"Pyth\" ./iptables/Pyth.sh\n\n"

	"sudo ip netns exec \"Stev\" ./iptables/Stev.sh\n\n"

	"sudo ip netns exec \"SH1C\" ./iptables/SH1C.sh\n\n"

	"sudo ip netns exec \"Carn\" ./iptables/Carn.sh\n\n"

	"sudo ip netns exec \"Mich\" ./iptables/Mich.sh\n\n"

	"echo \"All the firewalls have been set !\"\n\n"

	"exit 0")
iptables_file.close()
os.chmod(PATH+"iptables/launchfirewall.sh", 0o766)
	##########

####################routerfirewall.sh###############################"
with open(PATH+'firewall_configuration_file.json') as data_file:
	data = json.load(data_file)


for router, configs_firewall in data.items():
	#pprint(router)
	router_firewall_config_file = open(PATH+"iptables/"+router+".sh", "w")

	router_firewall_config_file.write(
		"#!/bin/bash\n"
		"#Document generates by script firewall_config_creation.py, have a look on this python script for more details\n\n\n"

		"#Reinitialize the configuration\n"
		"ip6tables -F\n"
		"ip6tables -X\n"
		
		"# Flush all rules and delete all chains\n"
		"# because it is best to startup cleanly\n"
		"#ip6tables -F INPUT\n"
		"#ip6tables -F OUTPUT\n"
		"#ip6tables -F FORWARD\n"

	        "#DROP Polycies\n"
        	"ip6tables -P INPUT DROP\n"
        	"ip6tables -P FORWARD DROP\n"
        	"ip6tables -P OUTPUT DROP\n\n"

		"# Required for the loopback interface\n"
		"ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
		"ip6tables -A INPUT -i lo -j ACCEPT\n"
		"ip6tables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
		"ip6tables -A OUTPUT -o lo -j ACCEPT\n"
		"ip6tables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
		
		
		"#Define our policy\n"
		"# Reject connection attempts not initiated from the host\n"
		"#ip6tables -A INPUT -p tcp --syn -j DROP\n\n"
		
		"#Enable TCP, UDP\n"
		"ip6tables -A INPUT -p tcp -j ACCEPT\n"
		"ip6tables -A FORWARD -p tcp -j ACCEPT\n"
		"ip6tables -A OUTPUT -p tcp -j ACCEPT\n"
		"ip6tables -A INPUT -p udp -j ACCEPT\n"
		"ip6tables -A FORWARD -p udp -j ACCEPT\n"
		"ip6tables -A OUTPUT -p udp -j ACCEPT\n"

		"#allow OSPF\n"
		"ip6tables -A INPUT -p 89 -j ACCEPT\n"
		"ip6tables -A OUTPUT -p 89 -j ACCEPT\n"
		"ip6tables -A FORWARD -p 89 -j ACCEPT\n\n"
		
		"#Authorize outgoing and incoming ping\n"
		"ip6tables -A INPUT -p icmpv6 -j ACCEPT\n"
		"ip6tables -A OUTPUT -p icmpv6 -j ACCEPT\n"
		"ip6tables -A FORWARD -p icmpv6 -j ACCEPT\n"
		
		"#Allow Traceroute\n"
		"ip6tables -I INPUT -p udp --sport 33434:33524 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT\n\n"
		
		"# Allow logging in via SSH\n"
		"#ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT\n\n"
		"# Restrict incoming SSH to a specific network interface\n"
		"for a in 200 300\n"
		"do\n"
		"		ip6tables -A INPUT -i "+router+"-eth1 -p tcp --dport 22 -j ACCEPT\n"
		"		ip6tables -I OUTPUT -o  "+router+"-eth1 -p udp --dport 33434:33524 -m state --state NEW -j ACCEPT\n"
		"		#Restrict incoming SSH to the local network\n"
		"		ip6tables -A INPUT -i "+router+"-eth1 -p tcp -s fd00:${a}:3::"+configs_firewall["router_id"]+"/48 --dport 22 -j ACCEPT\n\n"
	)
	if configs_firewall["bgp"] == "true":
		router_firewall_config_file.write(
		"		#allow BGP(router connected with provider)\n"
		"		ip6tables -A INPUT -p tcp -m tcp --dport 179 -j ACCEPT\n"
    	"		ip6tables -A OUTPUT -p tcp -m tcp --dport 179 -j ACCEPT\n" 
		"		ip6tables -A FORWARD -p tcp -m tcp --dport 179 -j ACCEPT\n"
		#"#		for k in 's' 'd'\n"
		#"#		do\n"
		#"#			ip6tables -A INPUT -${k} fd00:${a}::"+configs_firewall["suffixe_provider"]+"/48 -p tcp --${k}port 179 -j ACCEPT\n"
		#"#			ip6tables -A OUTPUT -${k} fd00:${a}::"+configs_firewall["suffixe_provider"]+"/48 -p tcp --${k}port 179 -j ACCEPT\n"
		#"#			ip6tables -A FORWARD -${k} fd00:${a}::"+configs_firewall["suffixe_provider"]+"/48 -p tcp --${k}port 179 -j ACCEPT\n"
		#"#		done\n"
		)
	router_firewall_config_file.write(
		"		ip6tables -A OUTPUT -p udp -d fd00:${a}:3:"+configs_firewall["suffixe_DNS"]+"/64 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT\n"
		"		ip6tables -A INPUT  -p udp -s fd00:${a}:3:"+configs_firewall["suffixe_DNS"]+"/64 --sport 53 -m state --state ESTABLISHED     -j ACCEPT\n"
		"		ip6tables -A OUTPUT -p tcp -d fd00:${a}:3:"+configs_firewall["suffixe_DNS"]+"/64 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT\n"
		"		ip6tables -A INPUT -p tcp -s fd00:${a}:3:"+configs_firewall["suffixe_DNS"]+"/64 --sport 53 -m state --state ESTABLISHED -j ACCEPT\n"
		"done\n"
		"# Allow external access to your HTTP and HTTPS server\n"
		"ip6tables -A INPUT -p tcp -m multiport --dports 80,443,8080 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT\n"
		"ip6tables -A OUTPUT -p tcp -m multiport --dports 80,443,8080 -m conntrack --ctstate ESTABLISHED -j ACCEPT\n\n"
		"# Allow external access to your unencrypted mail server, SMTP,IMAP, and Telnet.\n"
		"ip6tables -A INPUT -p tcp -m multiport --dports 25,110,143 -j ACCEPT\n"
		"#Print table from routers and display the rules added before"
		"ip6tables -L"
	)
	router_firewall_config_file.close()
	os.chmod(PATH+"iptables/"+router+".sh", 0o766)
