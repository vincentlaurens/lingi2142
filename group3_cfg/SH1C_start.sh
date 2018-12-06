#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip address add dev SH1C-eth0 fd00:200:3:f05::6/64 
ip address add dev SH1C-eth0 fd00:300:3:f05::6/64 
ip address add dev SH1C-eth1 fd00:200:3:f06::6/64 
ip address add dev SH1C-eth1 fd00:300:3:f06::6/64 

ip address add dev SH1C-lan1 fd00:200:3:f061::6/64 
ip address add dev SH1C-lan1 fd00:300:3:f061::6/64 


bird6 -s /tmp/SH1C_bird.ctl -P /tmp/SH1C_bird.pid 

snmpd &> /dev/null
