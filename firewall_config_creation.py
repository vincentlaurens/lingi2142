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

		"# Flush all rules and delete all chains\n"
		"# because it is best to startup cleanly\n"
		"#ip6tables -F INPUT\n"
		"#ip6tables -F OUTPUT\n"
		"#ip6tables -F FORWARD\n"
		"#Reinitialize the configuration\n"
		"ip6tables -F\n"
		"ip6tables -X\n"
		#"ip6tables -t filter -D INPUT -s 2001:db8::/32 -j DROP\n"
		#"ip6tables -t filter -D INPUT -s 2001:db8::/32 -j DROP\n"
		"#Define our policy"
		"ip6tables -P INPUT DROP\n"
		"ip6tables -P FORWARD DROP\n"
		"ip6tables -P OUTPUT DROP\n\n"
		"#Enable stateful inspection\n"
		"ip6tables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT\n"
		"ip6tables -A OUTPUT -m conntrack ! --ctstate INVALID -j ACCEPT\n"
		"ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
		"ip6tables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
		"ip6tables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT\n\n"
		"# Required for the loopback interface\n"
		"ip6tables -A INPUT -i lo -j ACCEPT\n"
		"ip6tables -A OUTPUT -o lo -j ACCEPT\n\n"
		"#ip6tables -A INPUT -p tcp -j ACCEPT\n"
		"#ip6tables -A FORWARD -p tcp -j ACCEPT\n"
		"#ip6tables -A OUTPUT -p tcp -j ACCEPT\n"
		"#ip6tables -A INPUT -p udp -j ACCEPT\n"
		"#ip6tables -A FORWARD -p udp -j ACCEPT\n"
		"#ip6tables -A OUTPUT -p udp -j ACCEPT\n"
		"# Reject connection attempts not initiated from the host\n"
		"#ip6tables -A INPUT -p tcp --syn -j DROP\n\n"
		"#allow OSPF\n"
		"ip6tables -A INPUT -p 89 -j ACCEPT\n"
		"ip6tables -A OUTPUT -p 89 -j ACCEPT\n"
		"ip6tables -A FORWARD -p 89 -j ACCEPT\n\n"
		"#Authorize outgoing ping\n"
		"#ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-reply -j ACCEPT\n"
		"#ip6tables -A INPUT -p icmpv6 --icmpv6-type time-exceeded -j ACCEPT\n"
		"#ip6tables -A INPUT -p icmpv6 --icmpv6-type destination-unreachable -j ACCEPT\n"
		"#ip6tables -A OUTPUT -p icmpv6 --icmpv6-type echo-request -m limit --limit 50/min -j ACCEPT\n"
		"#ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-reply -m limit --limit 50/min -j ACCEPT\n"
		"#ip6tables -A OUTPUT -p icmpv6 -m limit --limit 5/second  -j ACCEPT\n"
		"#ip6tables -A OUTPUT -p icmpv6 --icmpv6-type echo-request -j ACCEPT\n\n"
		"#Authorize incoming pings\n"
		"#ip6tables -A OUTPUT -p icmpv6 --icmpv6-type echo-reply -j ACCEPT\n"
		"#ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -j ACCEPT\n"
		"#ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -m limit --limit 50/min -j ACCEPT\n"
		"#ip6tables -A OUTPUT -p icmpv6 --icmpv6-type echo-reply -m limit --limit 50/min -j ACCEPT\n"
		"#ip6tables -A OUTPUT -p icmpv6 --icmpv6-type destination-unreachable -j ACCEPT\n"
		"#Allow Traceroute\n"
		"ip6tables -I INPUT -p udp --sport 33434:33524 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT\n\n"
		"# Allow logging in via SSH\n"
		"ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT\n\n"
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
		"		for k in 'd' 's'\n"
		"		do\n"
		"			ip6tables -A INPUT -${k} fd00:$a::b -p tcp --${k}port 179 -j ACCEPT\n"
		"			ip6tables -A OUTPUT -${k} fd00:$a::b -p tcp --${k}port 179 -j ACCEPT\n"
		"			ip6tables -A FORWARD -${k} fd00:$a::b -p tcp --${k}port 179 -j ACCEPT\n"
		"		done\n"
		)
	router_firewall_config_file.write(
		"		ip6tables -A OUTPUT -p udp -d fd00:${a}:3:1000::1 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT\n"
		"		ip6tables -A INPUT  -p udp -s fd00:${a}:3:1000::1 --sport 53 -m state --state ESTABLISHED     -j ACCEPT\n"
		"		ip6tables -A OUTPUT -p tcp -d fd00:${a}:3:1000::1 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT\n"
		"		ip6tables -A INPUT -p tcp -s fd00:${a}:3:1000::1 --sport 53 -m state --state ESTABLISHED -j ACCEPT\n"
		"done\n"
		"# Allow external access to your HTTP and HTTPS server\n"
		"sudo ip6tables -A INPUT -p tcp -m multiport --dports 80,443,8080 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT\n"
		"sudo ip6tables -A OUTPUT -p tcp -m multiport --dports 80,443,8080 -m conntrack --ctstate ESTABLISHED -j ACCEPT\n\n"
		"# Allow external access to your unencrypted mail server, SMTP,IMAP, and Telnet.\n"
		"ip6tables -A INPUT -p tcp -m multiport --dports 25,110,143 -j ACCEPT\n"
		"#Print table from routers and display the rules added before"
		"ip6tables -L"
	)
	router_firewall_config_file.close()
	os.chmod(PATH+"iptables/"+router+".sh", 0o766)
