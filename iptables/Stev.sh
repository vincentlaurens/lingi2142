#!/bin/bash
#Document generates by script firewall_config_creation.py, have a look on this python script for more details


# Flush all rules and delete all chains
# because it is best to startup cleanly
ip6tables -F
ip6tables -X
ip6tables -t nat -F
ip6tables -t nat -X
ip6tables -t mangle -F 
ip6tables-t mangle -X 
ip6tables -L

#all to Zero
ip6tables -Z
ip6tables -t nat -Z
ip6tables -t mangle -Z
ip6tables -t filter -D INPUT -s 2001:db8::/32 -j DROP
ip6tables -t filter -D INPUT -s 2001:db8::/32 -j DROP
ip6tables -P INPUT DROP
ip6tables -P FORWARD DROP
ip6tables -P OUTPUT ACCEPT

# Required for the loopback interface
ip6tables -A INPUT -i lo -j ACCEPT
ip6tables -A OUTPUT -o lo -j ACCEPT

# Reject connection attempts not initiated from the host
ip6tables -A INPUT -p tcp --syn -j DROP

#allow OSPF
ip6tables -A INPUT -p OSPF -j ACCEPT
ip6tables -A OUTPUT -p OSPF -j ACCEPT
ip6tables -A FORWARD -p OSPF -j ACCEPT

# Allow return connections initiated from the host
ip6tables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

#Authorize important ICMP Packet
ip6tables -A INPUT -p icmpv6 --icmp-type echo-request -j ACCEPT
ip6tables-A INPUT -p icmpv6 --icmp-type time-exceeded -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmp-type destination-unreachable -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -m limit --limit 50/min -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-reply -m limit --limit 50/min -j ACCEPT
ip6tables -A OUTPUT -p icmpv6 -m limit --limit 5/second  -j ACCEPT

#Allow Traceroute
ip6tables -I INPUT -p udp --sport 33434:33524 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

# Allow logging in via SSH
ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT

# Restrict incoming SSH to a specific network interface
for a in 200 300
do
		ip6tables -A INPUT -i Stev-eth1 -p tcp --dport 22 -j ACCEPT
		ipt6ables -I OUTPUT -o  Stev-eth1 -p udp --dport 33434:33524 -m state --state NEW -j ACCEPT
		#Restrict incoming SSH to the local network
		ip6tables -A INPUT -i Stev-eth1 -p tcp -s fd00:${a}:3::3/48 --dport 22 -j ACCEPT

			ip6tables -A OUTPUT -p udp -d fd00:${a}:3:1000::1 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
			ip6tables -A INPUT  -p udp -s fd00:${a}:3:1000::1 --sport 53 -m state --state ESTABLISHED     -j ACCEPT
			ip6tables -A OUTPUT -p tcp -d fd00:${a}:3:1000::1 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
			ip6tables -A INPUT -p tcp -s fd00:${a}:3:1000::1 --sport 53 -m state --state ESTABLISHED -j ACCEPT
done
# Allow external access to your HTTP and HTTPS server
sudo ip6tables -A INPUT -p tcp -m multiport --dports 80,443,8080 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo ip6tables -A OUTPUT -p tcp -m multiport --dports 80,443,8080 -m conntrack --ctstate ESTABLISHED -j ACCEPT

# Allow external access to your unencrypted mail server, SMTP,IMAP, and Telnet.
ip6tables -A INPUT -p tcp -m multiport --dports 25,110,143 -j ACCEPT
