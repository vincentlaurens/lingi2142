#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip link set dev belnetb up 
ip address add dev belnetb fd00:200::3/48  

ip link set dev Hall-eth0 up 
ip address add dev Hall-eth0 fd00:200:3:6::1/64 
ip address add dev Hall-eth0 fd00:300:3:6::1/64 
ip link set dev Hall-eth1 up 
ip address add dev Hall-eth1 fd00:200:3:0::1/64 
ip address add dev Hall-eth1 fd00:300:3:0::1/64 

ip link set dev Hall-lan0-Serv up 
ip address add dev Hall-lan0-Serv fd00:200:3:1000::1/64 
ip address add dev Hall-lan0-Serv fd00:300:3:1000::1/64 

bird6 -s /tmp/Hall_bird.ctl -P /tmp/Hall_bird.pid 
