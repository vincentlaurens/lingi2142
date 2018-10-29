#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip link set dev SH1C-eth0 up 
ip address add dev SH1C-eth0 fd00:200:3:5::6/64 
ip address add dev SH1C-eth0 fd00:300:3:5::6/64 
ip link set dev SH1C-eth1 up 
ip address add dev SH1C-eth1 fd00:200:3:6::6/64 
ip address add dev SH1C-eth1 fd00:300:3:6::6/64 


bird6 -s /tmp/SH1C_bird.ctl -P /tmp/SH1C_bird.pid 
