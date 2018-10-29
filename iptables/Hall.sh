#!/bin/bash
#Document generates by script firewall_config_creation.py, have a look on this python script for more details



#Reinitialize the configuration
ip6tables -F
ip6tables -X
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
ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A INPUT -i lo -j ACCEPT
ip6tables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A OUTPUT -o lo -j ACCEPT
ip6tables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
#Define our policy
# Reject connection attempts not initiated from the host
#ip6tables -A INPUT -p tcp --syn -j DROP

#Enable TCP, UDP
ip6tables -A INPUT -p tcp -j ACCEPT
ip6tables -A FORWARD -p tcp -j ACCEPT
ip6tables -A OUTPUT -p tcp -j ACCEPT
ip6tables -A INPUT -p udp -j ACCEPT
ip6tables -A FORWARD -p udp -j ACCEPT
ip6tables -A OUTPUT -p udp -j ACCEPT
#Authorize OSPF
ip6tables -A INPUT -p 89 -j ACCEPT
ip6tables -A OUTPUT -p 89 -j ACCEPT
ip6tables -A FORWARD -p 89 -j ACCEPT

#Authorize outgoing and incoming ping
ip6tables -A INPUT -p icmpv6 -j ACCEPT
ip6tables -A OUTPUT -p icmpv6 -j ACCEPT
ip6tables -A FORWARD -p icmpv6 -j ACCEPT
#limitation on 128/0
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -j ACCEPT --match limit --limit 5/minute
# Neighbor Solicitation limitation to avoid DoS
ip6tables -A INPUT -p icmpv6 --icmpv6-type 135/0 -j ACCEPT --match limit --limit 15/minute
#Authorize DHCPv6 on the local link on the client site
ip6tables -A INPUT -m state --state NEW -m udp -p udp --dport 546 -d fe80::/64 -j ACCEPT

#Allow Traceroute
ip6tables -I INPUT -p udp --sport 33434:33524 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

#Authorize incoming SSH connections with the unicast routing addresses on Internetip6tables -A INPUT -s 2000::/3 -p tcp --dport 22 --syn -m state --state NEW -j ACCEPT
# Allow logging in via SSH
#ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT

for a in 200 300
do
		#allow BGP(router connected with provider)
		ip6tables -A INPUT -p tcp -m tcp --dport 179 -j ACCEPT
		ip6tables -A OUTPUT -p tcp -m tcp --dport 179 -j ACCEPT
		ip6tables -A FORWARD -p tcp -m tcp --dport 179 -j ACCEPT
		ip6tables -A OUTPUT -p udp -d fd00:${a}:3:1000::53/64 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
		ip6tables -A INPUT  -p udp -s fd00:${a}:3:1000::53/64 --sport 53 -m state --state ESTABLISHED     -j ACCEPT
		ip6tables -A OUTPUT -p tcp -d fd00:${a}:3:1000::53/64 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
		ip6tables -A INPUT -p tcp -s fd00:${a}:3:1000::53/64 --sport 53 -m state --state ESTABLISHED -j ACCEPT
done
# Allow external access to your HTTP and HTTPS server
#ip6tables  -A INPUT -p tcp -m multiport --dports 80,443,8080 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
#ip6tables -A OUTPUT -p tcp -m multiport --dports 80,443,8080 -m conntrack --ctstate ESTABLISHED -j ACCEPT

# Allow external access to your unencrypted mail server, SMTP,IMAP, and Telnet.
ip6tables -A INPUT -p tcp -m multiport --dports 25,110,143 -j ACCEPT
#Print table from routers and display the rules added before
ip6tables -L
