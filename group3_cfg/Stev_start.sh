#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip address add dev Stev-eth0 fd00:200:3:f03::3/64 
ip address add dev Stev-eth0 fd00:300:3:f03::3/64 
ip address add dev Stev-eth1 fd00:200:3:f01::3/64 
ip address add dev Stev-eth1 fd00:300:3:f01::3/64 

ip address add dev Stev-lan1 fd00:200:3:f032::3/64 
ip address add dev Stev-lan1 fd00:300:3:f032::3/64 


bird6 -s /tmp/Stev_bird.ctl -P /tmp/Stev_bird.pid 

snmpd &> /dev/null
