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

# Allow return connections initiated from the host
ip6tables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

#Authorize important ICMP Packet
ip6tables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
ip6tables-A INPUT -p icmp --icmp-type time-exceeded -j ACCEPT
ip6tables -A INPUT -p icmp --icmp-type destination-unreachable -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-request -m limit --limit 50/min -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type echo-reply -m limit --limit 50/min -j ACCEPT
ip6tables -A OUTPUT -p icmp -m limit --limit 5/second  -j ACCEPT

# Allow logging in via SSH
ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT

# Restrict incoming SSH to a specific network interface
ip6tables -A INPUT -i $SH1C-eth1 -p tcp --dport 22 -j ACCEPT
# Restrict incoming SSH to the local network
ip6tables -A INPUT -i $SH1C-eth1 -p tcp -s fd00:300:3::1/48 --dport 22 -j ACCEPT
ip6tables -A INPUT -i $SH1C-eth1 -p tcp -s fd00:200:3::1/48 --dport 22 -j ACCEPT

# Allow external access to your HTTP server
ip6tables -A INPUT -p tcp -m multiport --dport 80,443,8080 -j ACCEPT

# Allow external access to your unencrypted mail server, SMTP,IMAP, and POP3.
ip6tables -A INPUT -p tcp -m multiport --dport 25,110,143 -j ACCEPT
