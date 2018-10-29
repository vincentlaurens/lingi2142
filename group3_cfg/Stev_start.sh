#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip link set dev Stev-eth0 up 
ip address add dev Stev-eth0 fd00:200:3:3::3/64 
ip address add dev Stev-eth0 fd00:300:3:3::3/64 
ip link set dev Stev-eth1 up 
ip address add dev Stev-eth1 fd00:200:3:1::3/64 
ip address add dev Stev-eth1 fd00:300:3:1::3/64 


bird6 -s /tmp/Stev_bird.ctl -P /tmp/Stev_bird.pid 
