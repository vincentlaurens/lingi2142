#group3 : firewall_config_creation.py - Python 3 - Read a parsed file (json)

import json
import os


from constants import PATH


####################restartfirewall.sh###############################"
iptables_file = open(PATH+"iptables/restartFirewall.sh", "w")
iptables_file.write("#!/bin/bash\n\n"
	"echo \"Starting the firewalls on all routers ...\"\n\n"

	"sudo ip netns exec \"Hall\" ./iptables/Hall.sh\n\n"

	"sudo ip netns exec \"Pyth\" ./iptables/Pyth.sh\n\n"

	"sudo ip netns exec \"Stev\" ./iptables/Stev.sh\n\n"

	"sudo ip netns exec \"SH1C\" ./iptables/SH1C.sh\n\n"

	"sudo ip netns exec \"Carn\" ./iptables/Carn.sh\n\n"

	"sudo ip netns exec \"Mich\" ./iptables/Mich.sh\n\n"

	"echo \"All the firewalls have been set !\"\n\n"

	"exit 0\n")
iptables_file.close()
os.chmod(PATH+"iptables/restartFirewall.sh", 0o766)
	##########

####################routerfirewall.sh###############################"
with open(PATH+'firewall_configuration_file.json') as data_file:
	data = json.load(data_file)


for router, configs_firewall in data.items():
	router_firewall_config_file = open(PATH+"iptables/"+router+".sh", "w")

	router_firewall_config_file.write(
		"#!/bin/bash\n"
		"#Document generates by script firewall_config_creation.py, have a look on this python script for more details\n\n\n"
		
		"#Definition of variable\n"
		"DNS1_200=\"fd00:200:3:"+configs_firewall["suffixe_DNS"]+"/64\"\n"
		"DNS1_300=\"fd00:300:3:"+configs_firewall["suffixe_DNS"]+"/64\"\n"
		"DNS2_200=\"fd00:200:3:"+configs_firewall["suffixe_DNS2"]+"/64\"\n"
		"DNS2_300=\"fd00:300:3:"+configs_firewall["suffixe_DNS2"]+"/64\"\n\n"

		"#Reinitialize the configuration\n"
		"ip6tables -F\n"
		"ip6tables -X\n"
		"ip6tables -Z\n"
		
		"# Flush all rules and delete all chains\n"
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
		"ip6tables -A INPUT -i lo -j ACCEPT\n"
		"ip6tables -A OUTPUT -o lo -j ACCEPT\n\n"
        "#Related and Established connections\n"
		"ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
		"ip6tables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
		"ip6tables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
		
		
		"#Define our policy\n"
		"# Reject connection attempts not initiated from the host\n"
		"#ip6tables -A INPUT -p tcp --syn -j DROP\n\n"

		"#Authorize OSPF\n"
		"ip6tables -A INPUT -p 89 -j ACCEPT\n"
		"ip6tables -A OUTPUT -p 89 -j ACCEPT\n\n"
		
		"# Drop INVALID packets\n"
   		"ip6tables -A INPUT -m state --state INVALID -j DROP\n"
		"ip6tables -A OUTPUT -m state --state INVALID -j DROP\n"
		"ip6tables -A FORWARD -m state --state INVALID -j DROP\n\n"

		# "ip6tables -A INPUT ! -p icmpv6 -m state --state INVALID -j DROP\n"
		# "ip6tables -A OUTPUT ! -p icmpv6 -m state --state INVALID -j DROP\n"
		# "ip6tables -A FORWARD ! -p icmpv6 -m state --state INVALID -j DROP\n\n"
		
		"#limitation on 128/0\n"
		"ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -m limit --limit 5/second -j ACCEPT\n"
		"# Neighbor Solicitation limitation to avoid DoS\n"
		"ip6tables -A INPUT -p icmpv6 --icmpv6-type 135/0 -m limit --limit 15/second -j ACCEPT\n"

		"#Authorize outgoing and incoming ping\n"
		"ip6tables -A INPUT -p icmpv6 -j ACCEPT\n"
		"ip6tables -A OUTPUT -p icmpv6 -j ACCEPT\n"
		"ip6tables -A FORWARD -p icmpv6 -j ACCEPT\n"

		"# Allow SNMP\n"
		"for p in \"udp\"\n"
		"do\n"
		"	for e in \"d\"\n"
		"	do\n"
		"		ip6tables -A INPUT -p $p -m $p --${e}port 161 -j ACCEPT\n"
		"		ip6tables -A FORWARD -p $p -m $p --${e}port 161 -j ACCEPT\n"
		"		ip6tables -A OUTPUT -p $p -m $p --${e}port 161 -j ACCEPT\n"
		"	done\n"
		"done\n"
		"ip6tables -A INPUT -p udp -m udp --dport 162 -j ACCEPT\n"
		"ip6tables -A FORWARD -p udp -m udp --dport 162 -j ACCEPT\n"
		"ip6tables -A OUTPUT -p udp -m udp --dport 162 -j ACCEPT\n\n"
                                                                  
		"#Allow DNS server\n"
		"for x in $DNS1_200 $DNS1_300 $DNS2_200 $DNS2_300\n"
		"do\n"
		"  for e in \"udp\" \"tcp\"\n"
        "  do\n"
		"     ip6tables -A INPUT  -p $e -s $x --source-port 53 -m state --state ESTABLISHED -j ACCEPT\n"
		"     ip6tables -A OUTPUT -p $e -d $x --destination-port 53 -m state --state NEW,ESTABLISHED -j ACCEPT\n"
		"  done\n"
		"done\n\n"
                                                                  
        "#Authorize DHCPv6 on the local link on the client site\n"
		"ip6tables -A INPUT -m state --state NEW -m udp -p udp --destination-port 546 -d fe80::/64 -j ACCEPT\n\n"
        "# Allow DHCP requests from the clients to the server\n"
        "ip6tables -A INPUT -p udp --sport 546 --dport 547 -j ACCEPT\n"
		"ip6tables -A OUTPUT -p udp --sport 546 --dport 547 -j ACCEPT\n"
		"ip6tables -A FORWARD -p udp --sport 546 --dport 547 -j ACCEPT\n"
        "# Allow DHCP response from the server to the clients\n"
        "ip6tables -A INPUT -p udp --sport 547 --dport 546 -j ACCEPT\n"
		"ip6tables -A OUTPUT -p udp --sport 547 --dport 546 -j ACCEPT\n"
		"ip6tables -A FORWARD -p udp --sport 547 --dport 546 -j ACCEPT\n\n"
		
		# "#Allow Tunneling (encapsulation)\n"
		# "ip6tables  -A FORWARD -p 41 -j ACCEPT\n"
		
		"#Allow Traceroute\n"
		"ip6tables -I INPUT -p udp --source-port 33434:33524 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT\n\n"
		
		"#Authorize incoming SSH connections with the unicast routing addresses on Internet\n"
		"ip6tables -A INPUT -s 2000::/3 -p tcp --destination-port 22 --syn -m state --state NEW -j ACCEPT\n"
		
		
		"# Allow logging in via SSH\n"
		"#ip6tables -A INPUT -p tcp --destination-port 22 -j ACCEPT\n\n"
	)
	if "lans" in configs_firewall:
		if "Stud" and "Staff" in configs_firewall:
			router_firewall_config_file.write(
				"for a in 200 300\n"
				"do\n"
				"	# Refuse router advertisement from students (flooding or misbehaviour) for $a\n"
				"	ip6tables -A INPUT -s fd00:$a:3:"+configs_firewall["Stud"]+"::/64 -p icmpv6 --icmpv6-type 134/0 -j REJECT --reject-with icmp-host-prohibited\n"
				"	ip6tables -A INPUT -s fd00:$a:3:"+configs_firewall["Staff"]+"::/64 -p icmpv6 --icmpv6-type 134/0 -j REJECT --reject-with icmp-host-prohibited\n"
		
																				 
				#"	# Block student and staff from connecting with each other for $a: This isn't necessary but They show that this kind of connexions is forbidden\n"
				#"	ip6tables -A FORWARD -s fd00:$a:3:"+configs_firewall["Stud"]+"::/64 -d fd00:$a:3:"+configs_firewall["Staff"]+"::/64 -j DROP\n"
				#"	ip6tables -A FORWARD -s fd00:$a:3:"+configs_firewall["Staff"]+"::/64 -d fd00:$a:3:"+configs_firewall["Stud"]+"::/64 -j DROP\n\n"

				"	# Accept FTP between two Staff hosts or between two Studs hosts and between Staff and Stud and Stud and Staff\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Stud"]+"::/64 -d fd00:$a:3:"+configs_firewall["Stud"]+"::/64 --destination-port 21  -j ACCEPT\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Staff"]+"::/64 -d fd00:$a:3:"+configs_firewall["Staff"]+"::/64 --destination-port 21  -j ACCEPT\n"
                "	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Staff"]+"::/64 -d fd00:$a:3:"+configs_firewall["Stud"]+"::/64 --destination-port 21  -j ACCEPT\n"
                "	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Stud"]+"::/64 -d fd00:$a:3:"+configs_firewall["Staff"]+"::/64 --destination-port 21  -j ACCEPT\n"
																																																																							 
				"	# Allow SSH for students and staff members for $a\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Stud"]+"::/64 --destination-port 22 -j ACCEPT\n\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Staff"]+"::/64 --destination-port 22 -j ACCEPT\n\n"
				
				"	# Allow SMTP for students and staff members for $a\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Stud"]+"::/64 --destination-port 25 -j ACCEPT\n\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Staff"]+"::/64 --destination-port 25 -j ACCEPT\n\n"
				
				"	# Allow HTTP and HTTPS for students and staff members for $a\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Stud"]+"::/64 --destination-port 80 -j ACCEPT\n\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Staff"]+"::/64 --destination-port 80 -j ACCEPT\n\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Stud"]+"::/64 --destination-port 443 -j ACCEPT\n\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["Staff"]+"::/64 --destination-port 443 -j ACCEPT\n\n"
				"done\n\n"
			)
		if "Monitoring" in configs_firewall:
			router_firewall_config_file.write(
				"#Allow SNMP for each hosts on Monitoring LAN and mailbox protocols and SSH for check log for instance\n"
				"for a in 200 300\n"
				"do\n"
				"	ip6tables -A INPUT -p tcp -d fd00:$a:3:"+configs_firewall["Monitoring"]+"::1/64 -m tcp --destination-port 546 -j ACCEPT\n"
				"	ip6tables -A INPUT -p udp -d fd00:$a:3:"+configs_firewall["Monitoring"]+"::1/64 -m udp --destination-port 547 -j ACCEPT\n"
				"	ip6tables -A INPUT -p tcp -d fd00:$a:3:"+configs_firewall["Monitoring"]+"::1/64 -m tcp --destination-port 22 -j ACCEPT\n"	
				"	ip6tables -A INPUT -p tcp -d fd00:$a:3:"+configs_firewall["Monitoring"]+"::1/64 -m multiport --destination-ports 25,110,143 -j ACCEPT\n\n"
				"done\n\n"
			)
		if "visitor" in configs_firewall:
			router_firewall_config_file.write(
				"# Allow HTTP and HTTPS for visitor\n"
				"# Allow DNS for visitor\n"
				"for a in 200 300\n"
				"do\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["visitor"]+"::/64 --destination-port 80 -j ACCEPT\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["visitor"]+"::/64 --destination-port 443 -j ACCEPT\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["visitor"]+"::/64 -d fd00:$a:3:"+configs_firewall["suffixe_DNS"]+"/64 --destination-port 53 -j ACCEPT\n"
				"	ip6tables -A FORWARD -p tcp -s fd00:$a:3:"+configs_firewall["visitor"]+"::/64 -d fd00:$a:3:"+configs_firewall["suffixe_DNS2"]+"/64 --destination-port 53 -j ACCEPT\n"
				"done\n\n"
			)
		
	router_firewall_config_file.write(
		"# Restrict incoming SSH to a specific network interface\n"
		"ip6tables -A INPUT -i "+router+"-eth1 -p tcp --destination-port 22 -j ACCEPT\n"
		"ip6tables -A OUTPUT -o  "+router+"-eth1 -p udp --destination-port 33434:33524 -m state --state NEW -j ACCEPT\n"
        "for a in 200 300\n"
        "do\n"
		"	#Restrict incoming SSH to the local network\n"
		"	ip6tables -A INPUT -i "+router+"-eth1 -p tcp -s fd00:$a:3::"+configs_firewall["router_id"]+"/48 --destination-port 22 -j ACCEPT\n\n"
		"done\n\n"
	)
	if configs_firewall["bgp"] == "true":
		if router == "Hall":
			router_firewall_config_file.write(
				"#allow external BGP(router connected with provider)\n"
				"for p in \"tcp\"\n"
				"do\n"		
				"	ip6tables -A INPUT -i belnetb -p $p  --destination-port 179 -j ACCEPT\n"
				"	ip6tables -A INPUT -i belnetb -p $p  --source-port 179 -j ACCEPT\n"
				"	ip6tables -A OUTPUT -o belnetb -p $p  --destination-port 179 -j ACCEPT\n" 
				"done\n"
				"#Drop OSPF between Pyth and provider\n"
				"ip6tables -A INPUT -i belnetb  -p 89 -j DROP\n" #-s fd00:300::b/64
				"ip6tables -A OUTPUT -o belnetb -p 89 -j DROP\n\n" #-s fd00:300::b/64
				"ip6tables -A OUTPUT -o  belnetb -p udp --destination-port 33434:33524 -m state --state NEW -j DROP\n"
				"for a in 200 300\n"
				"do\n"
				"	#Drop inner address from the outside\n "
				"	ip6tables -A INPUT -i belnetb -s fd00:$a:3::/48 -j DROP\n"
				"	#DROP SNMP\n"
				"	for p in \"udp\"\n"
				"	do\n"
				"	   for e in \"s\" \"d\"\n"
				"		do\n"
				"			ip6tables -A INPUT -i belnetb  -p $p -d fd00:$a:3:f02f::1/64 -m $p --${e}port 161 -j DROP\n"
				"			ip6tables -A INPUT -i belnetb -p $p -d fd00:$a:3:f02f::1/64 -m $p --${e}port 162 -j DROP\n"
				"		done\n"
				"	done\n"
				"done\n\n"
				"#DROP DHCPv6 comming from and going over Internet\n"
				"for c in 546 547\n"
				"do\n"
				"	ip6tables -A INPUT -i belnetb -p udp -m udp --destination-port $c -j DROP\n"
				"	ip6tables -A FORWARD -i belnetb -p udp -m udp --destination-port $c -j DROP\n"	
				"	ip6tables -A OUTPUT -o belnetb -p udp -m udp --destination-port $c -j DROP\n"
				"	ip6tables -A FORWARD -o belnetb -p udp -m udp --destination-port $c -j DROP\n"
				"done\n"
				# "	#Allow IP encapsulation (tunneling)\n"
				# "	ip6tables  -A INPUT -p 41 -j ACCEPT\n"
				# "	ip6tables  -A OUTPUT -p 41 -j ACCEPT\n"
		)
		if router == "Pyth":
			router_firewall_config_file.write(
				"#allow external BGP(router connected with provider)\n"
				"for p in \"tcp\"\n"
				"do\n"
				"	ip6tables -A INPUT -i belneta -p $p  --destination-port 179 -j ACCEPT\n"
				"	ip6tables -A INPUT -i belneta -p $p  --source-port 179 -j ACCEPT\n"
				"	ip6tables -A OUTPUT -o belneta -p $p --destination-port 179 -j ACCEPT\n" 
				"done\n"
				"#Drop OSPF between Pyth and provider"
				"ip6tables -A INPUT -i belneta  -p 89 -j DROP\n" #-s fd00:200::b/64
				"ip6tables -A OUTPUT -o belneta -p 89 -j DROP\n" #-s fd00:200::b/64
				"ip6tables -A OUTPUT -o  belneta -p udp --destination-port 33434:33524 -m state --state NEW -j DROP\n\n"
				"for a in 200 300\n"
				"do\n"
				"	#Drop inner address from the outside\n "
				"	ip6tables -A INPUT -i belneta -s fd00:$a:3::/48 -j DROP\n\n"
	            "	#DROP SNMP\n"
	            "	for p in \"udp\"\n"
	            "	do\n"
	            "	   for e in \"s\" \"d\"\n"
	            "		do\n"
	            "		    ip6tables -A INPUT -i belneta  -p $p -d fd00:$a:3:f02f::1/64 -m $p --${e}port 161 -j DROP\n"
				"		    ip6tables -A INPUT -i belneta -p $p -d fd00:$a:3:f02f::1/64 -m $p --${e}port 162 -j DROP\n"
	            "		done\n"
	            "	done\n"
				"done\n\n"
				"#DROP DHCPv6 comming from and going over Internet\n"
				"for c in 546 547\n"
				"do\n"
				"	ip6tables -A INPUT -i belneta -p udp -m udp --destination-port $c -j DROP\n"
				"	ip6tables -A FORWARD -i belneta -p udp -m udp --destination-port $c -j DROP\n"	
				"	ip6tables -A OUTPUT -o belneta -p udp -m udp --destination-port $c -j DROP\n"
				"	ip6tables -A FORWARD -o belneta -p udp -m udp --destination-port $c -j DROP\n"
				"done\n\n"
				# "	#Allow IP encapsulation (tunneling)\n"
	            # "	ip6tables  -A INPUT -p 41 -j ACCEPT\n"
	            # "	ip6tables  -A OUTPUT -p 41 -j ACCEPT\n"
		    )
	router_firewall_config_file.write(
		"# Allow external access to your HTTP and HTTPS server\n"
		"#ip6tables  -A INPUT -p tcp -m multiport --destination-ports 80,443,8080 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT\n"
		"#ip6tables -A OUTPUT -p tcp -m multiport --destination-ports 80,443,8080 -m conntrack --ctstate ESTABLISHED -j ACCEPT\n\n"
		"# Allow external access to your unencrypted mail server, SMTP,IMAP, and Telnet.\n"
		"#ip6tables -A INPUT -p tcp -m multiport --destination-ports 25,110,143 -j ACCEPT\n\n"
		"# Record all dropped packets in files\n"
		"ip6tables -N LOGGING\n"
		"ip6tables -A INPUT -j LOGGING\n"
		"ip6tables -A OUTPUT -j LOGGING\n"
		"ip6tables -A FORWARD -j LOGGING\n"
		"ip6tables -A LOGGING -m limit --limit 10/minute -j LOG --log-prefix \"IP6Tables-Dropped: \" --log-level 4\n"
		"ip6tables -A LOGGING -j DROP\n"
		"#Print table from routers and display the rules added before in log\n"
		"ip6tables -L > group3_cfg/"+router+"/log/iptables_log\n"
		"echo [INFO SECURITY: "+router+"] Firewall set up!\n"
	)
	router_firewall_config_file.close()
	os.chmod(PATH+"iptables/"+router+".sh", 0o766)
