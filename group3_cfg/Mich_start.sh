#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip address add dev Mich-eth0 fd00:200:3:f05::5/64 
ip address add dev Mich-eth0 fd00:300:3:f05::5/64 
ip address add dev Mich-eth1 fd00:200:3:f04::5/64 
ip address add dev Mich-eth1 fd00:300:3:f04::5/64 



bird6 -s /tmp/Mich_bird.ctl -P /tmp/Mich_bird.pid 

snmpd &> /dev/null
