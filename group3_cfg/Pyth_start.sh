#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip address add dev belneta fd00:300::3/48  

ip address add dev Pyth-eth2 fd00:200:3:f01::2/64 
ip address add dev Pyth-eth2 fd00:300:3:f01::2/64 
ip address add dev Pyth-eth0 fd00:200:3:f00::2/64 
ip address add dev Pyth-eth0 fd00:300:3:f00::2/64 
ip address add dev Pyth-eth1 fd00:200:3:f02::2/64 
ip address add dev Pyth-eth1 fd00:300:3:f02::2/64 

ip address add dev Pyth-lan1 fd00:200:3:f02f::2/64 
ip address add dev Pyth-lan1 fd00:300:3:f02f::2/64 

ip -6 rule add from fd00:300:3::/48 to fd00:200:3::/48 pref 1000 table main
ip -6 rule add from fd00:300:3::/48 to fd00:300:3::/48 pref 1000 table main
ip -6 route add ::/0 via fd00:200:f01::1 dev Pyth-eth0 metric 1 table 10
ip -6 rule add from fd00:300:3::/48 pref 2000 table 10
ip -6 tunnel add toHall mode ip6ip6 remote fd00:300:3:f01::2 local fd00:300:3:f00::1 dev Pyth-eth0
ip link set dev toHall up

bird6 -s /tmp/Pyth_bird.ctl -P /tmp/Pyth_bird.pid 

snmpd &> /dev/null
