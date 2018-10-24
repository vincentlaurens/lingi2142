#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip link set dev belnetb up 
ip address add dev belnetb fd00:200::3/48  

ip link set dev Halles-eth0 up 
ip address add dev Halles-eth0 fd00:200:3:6::1/64 
ip address add dev Halles-eth0 fd00:300:3:6::1/64 

ip link set dev Halles-eth1 up 
ip address add dev Halles-eth1 fd00:200:3:0::1/64 
ip address add dev Halles-eth1 fd00:300:3:0::1/64 

bird6 -s /tmp/Halles_bird.ctl -P /tmp/Halles_bird.pid 
