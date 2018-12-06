#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip address add dev belnetb fd00:200::3/48  

ip address add dev Hall-eth0 fd00:200:3:f06::1/64 
ip address add dev Hall-eth0 fd00:300:3:f06::1/64 
ip address add dev Hall-eth1 fd00:200:3:f00::1/64 
ip address add dev Hall-eth1 fd00:300:3:f00::1/64 


ip -6 rule add from fd00:200:3::/48 to fd00:200:3::/48 pref 1000 table main
ip -6 rule add from fd00:200:3::/48 to fd00:300:3::/48 pref 1000 table main
ip -6 route add ::/0 via fd00:200:3:f01::2 dev Hall-eth1 metric 1 table 10
ip -6 rule add from fd00:200:3::/48 pref 2000 table 10
ip -6 tunnel add toPyth mode ip6ip6 remote fd00:300:3:f00::1 local fd00:300:3:f01::2 dev Hall-eth1
ip link set dev toPyth up

bird6 -s /tmp/Hall_bird.ctl -P /tmp/Hall_bird.pid 

snmpd &> /dev/null
