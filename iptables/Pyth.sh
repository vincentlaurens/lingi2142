#!/bin/bash
#Document generates by script firewall_config_creation.py, have a look on this python script for more details


#Definition of variable
DNS1_200="fd00:200:3:f011::53/64"
DNS1_300="fd00:300:3:f011::53/64"
DNS2_200="fd00:200:3:f012::53/64"
DNS2_300="fd00:300:3:f012::53/64"

#Reinitialize the configuration
ip6tables -F
ip6tables -X
ip6tables -Z
# Flush all rules and delete all chains
# Flush all rules and delete all chains
# because it is best to startup cleanly
#ip6tables -F INPUT
#ip6tables -F OUTPUT
#ip6tables -F FORWARD
#DROP Polycies
ip6tables -P INPUT DROP
ip6tables -P FORWARD DROP
ip6tables -P OUTPUT DROP

# Required for the loopback interface
ip6tables -A INPUT -i lo -j ACCEPT
ip6tables -A OUTPUT -o lo -j ACCEPT

#Related and Established connections
ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
#Define our policy
# Reject connection attempts not initiated from the host
#ip6tables -A INPUT -p tcp --syn -j DROP

#Authorize OSPF
ip6tables -A INPUT -p 89 -j ACCEPT
ip6tables -A OUTPUT -p 89 -j ACCEPT

# Drop INVALID packets
ip6tables -A INPUT -m state --state INVALID -j DROP
ip6tables -A OUTPUT -m state --state INVALID -j DROP
ip6tables -A FORWARD -m state --state INVALID -j DROP

#limitation on 128/0
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -m limit --limit 5/second -j ACCEPT
# Neighbor Solicitation limitation to avoid DoS
ip6tables -A INPUT -p icmpv6 --icmpv6-type 135/0 -m limit --limit 15/second -j ACCEPT
#Authorize outgoing and incoming ping
ip6tables -A INPUT -p icmpv6 -j ACCEPT
ip6tables -A OUTPUT -p icmpv6 -j ACCEPT
ip6tables -A FORWARD -p icmpv6 -j ACCEPT
# Allow SNMP
for p in "udp"
do
	for e in "d"
	do
		ip6tables -A INPUT -p $p -m $p --${e}port 161 -j ACCEPT
		ip6tables -A FORWARD -p $p -m $p --${e}port 161 -j ACCEPT
		ip6tables -A OUTPUT -p $p -m $p --${e}port 161 -j ACCEPT
	done
done
ip6tables -A INPUT -p udp -m udp --dport 162 -j ACCEPT
ip6tables -A FORWARD -p udp -m udp --dport 162 -j ACCEPT
ip6tables -A OUTPUT -p udp -m udp --dport 162 -j ACCEPT

#Allow DNS server
for x in $DNS1_200 $DNS1_300 $DNS2_200 $DNS2_300
do
  for e in "udp" "tcp"
  do
     ip6tables -A INPUT  -p $e -s $x --source-port 53 -m state --state ESTABLISHED -j ACCEPT
     ip6tables -A OUTPUT -p $e -d $x --destination-port 53 -m state --state NEW,ESTABLISHED -j ACCEPT
  done
done

#Authorize DHCPv6 on the local link on the client site
ip6tables -A INPUT -m state --state NEW -m udp -p udp --destination-port 546 -d fe80::/64 -j ACCEPT

# Allow DHCP requests from the clients to the server
ip6tables -A INPUT -p udp --sport 546 --dport 547 -j ACCEPT
ip6tables -A OUTPUT -p udp --sport 546 --dport 547 -j ACCEPT
ip6tables -A FORWARD -p udp --sport 546 --dport 547 -j ACCEPT
# Allow DHCP response from the server to the clients
ip6tables -A INPUT -p udp --sport 547 --dport 546 -j ACCEPT
ip6tables -A OUTPUT -p udp --sport 547 --dport 546 -j ACCEPT
ip6tables -A FORWARD -p udp --sport 547 --dport 546 -j ACCEPT

#Allow Traceroute
ip6tables -I INPUT -p udp --source-port 33434:33524 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

#Authorize incoming SSH connections with the unicast routing addresses on Internet
ip6tables -A INPUT -s 2000::/3 -p tcp --destination-port 22 --syn -m state --state NEW -j ACCEPT
# Allow logging in via SSH
#ip6tables -A INPUT -p tcp --destination-port 22 -j ACCEPT

for a in 200 300
do
	# Refuse router advertisement from students (flooding or misbehaviour) for $a
	ip6tables -A INPUT -s fd00:$a:3:f014::/64 -p icmpv6 --icmpv6-type 134/0 -j REJECT
	ip6tables -A INPUT -s fd00:$a:3:f015::/64 -p icmpv6 --icmpv6-type 134/0 -j REJECT
	# Accept FTP between two Staff hosts or between two Studs hosts and between Staff and Stud and Stud and Staff
	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f014::/64 -d fd00:$a:3:f014::/64 --destination-port 21  -j ACCEPT
	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f015::/64 -d fd00:$a:3:f015::/64 --destination-port 21  -j ACCEPT
	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f015::/64 -d fd00:$a:3:f014::/64 --destination-port 21  -j ACCEPT
	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f014::/64 -d fd00:$a:3:f015::/64 --destination-port 21  -j ACCEPT
	# Allow SSH for students and staff members for $a
	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f014::/64 --destination-port 22 -j ACCEPT
	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f015::/64 --destination-port 22 -j ACCEPT
	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f015::/64 -d fd00:$a:3:f014::/64 --destination-port 22 -j DROP

	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f014::/64 -d fd00:$a:3:f015::/64 --destination-port 22 -j DROP

	# Allow SMTP for students and staff members for $a
	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f014::/64 --destination-port 25 -j ACCEPT

	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f015::/64 --destination-port 25 -j ACCEPT

	# Allow HTTP and HTTPS for students and staff members for $a
	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f014::/64 --destination-port 80 -j ACCEPT

	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f015::/64 --destination-port 80 -j ACCEPT

	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f014::/64 --destination-port 443 -j ACCEPT

	ip6tables -A FORWARD -p tcp -s fd00:$a:3:f015::/64 --destination-port 443 -j ACCEPT

done

#Allow SNMP for each hosts on Monitoring LAN and mailbox protocols and SSH for check log for instance
for a in 200 300
do
	ip6tables -A INPUT -p tcp -d fd00:$a:3:f02f::1/64 -m tcp --destination-port 546 -j ACCEPT
	ip6tables -A INPUT -p udp -d fd00:$a:3:f02f::1/64 -m udp --destination-port 547 -j ACCEPT
	ip6tables -A INPUT -p tcp -d fd00:$a:3:f02f::1/64 -m tcp --destination-port 22 -j ACCEPT
	ip6tables -A INPUT -p tcp -d fd00:$a:3:f02f::1/64 -m multiport --destination-ports 25,110,143 -j ACCEPT

done

# Restrict incoming SSH to a specific network interface
ip6tables -A INPUT -i Pyth-eth1 -p tcp --destination-port 22 -j ACCEPT
ip6tables -A OUTPUT -o  Pyth-eth1 -p udp --destination-port 33434:33524 -m state --state NEW -j ACCEPT
for a in 200 300
do
	#Restrict incoming SSH to the local network
	ip6tables -A INPUT -i Pyth-eth1 -p tcp -s fd00:$a:3::2/48 --destination-port 22 -j ACCEPT

done

#allow external BGP(router connected with provider)
for p in "tcp"
do
	ip6tables -A INPUT -i belneta -p $p  --destination-port 179 -j ACCEPT
	ip6tables -A INPUT -i belneta -p $p  --source-port 179 -j ACCEPT
	ip6tables -A OUTPUT -o belneta -p $p --destination-port 179 -j ACCEPT
done
#Drop OSPF between Pyth and providerip6tables -A INPUT -i belneta  -p 89 -j DROP
ip6tables -A OUTPUT -o belneta -p 89 -j DROP
ip6tables -A OUTPUT -o  belneta -p udp --destination-port 33434:33524 -m state --state NEW -j DROP

for a in 200 300
do
	#Drop inner address from the outside
 	ip6tables -A INPUT -i belneta -s fd00:$a:3::/48 -j DROP

	#DROP SNMP
	for p in "udp"
	do
	   for e in "s" "d"
		do
		    ip6tables -A INPUT -i belneta  -p $p -d fd00:$a:3:f02f::1/64 -m $p --${e}port 161 -j DROP
		    ip6tables -A INPUT -i belneta -p $p -d fd00:$a:3:f02f::1/64 -m $p --${e}port 162 -j DROP
		done
	done
done

#DROP DHCPv6 comming from and going over Internet
for c in 546 547
do
	ip6tables -A INPUT -i belneta -p udp -m udp --destination-port $c -j DROP
	ip6tables -A FORWARD -i belneta -p udp -m udp --destination-port $c -j DROP
	ip6tables -A OUTPUT -o belneta -p udp -m udp --destination-port $c -j DROP
	ip6tables -A FORWARD -o belneta -p udp -m udp --destination-port $c -j DROP
done

# Allow external access to your HTTP and HTTPS server
#ip6tables  -A INPUT -p tcp -m multiport --destination-ports 80,443,8080 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
#ip6tables -A OUTPUT -p tcp -m multiport --destination-ports 80,443,8080 -m conntrack --ctstate ESTABLISHED -j ACCEPT

# Allow external access to your unencrypted mail server, SMTP,IMAP, and Telnet.
#ip6tables -A INPUT -p tcp -m multiport --destination-ports 25,110,143 -j ACCEPT

# Record all dropped packets in files
ip6tables -N LOGGING
ip6tables -A INPUT -j LOGGING
ip6tables -A OUTPUT -j LOGGING
ip6tables -A FORWARD -j LOGGING
ip6tables -A LOGGING -m limit --limit 10/minute -j LOG --log-prefix "IP6Tables-Dropped: " --log-level 4
ip6tables -A LOGGING -j DROP
#Print table from routers and display the rules added before in log
ip6tables -L > group3_cfg/Pyth/log/iptables_log
echo [INFO SECURITY: Pyth] Firewall set up!
