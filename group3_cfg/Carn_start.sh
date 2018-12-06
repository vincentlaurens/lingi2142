#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip address add dev Carn-eth2 fd00:200:3:f03::4/64 
ip address add dev Carn-eth2 fd00:300:3:f03::4/64 
ip address add dev Carn-eth0 fd00:200:3:f04::4/64 
ip address add dev Carn-eth0 fd00:300:3:f04::4/64 
ip address add dev Carn-eth1 fd00:200:3:f02::4/64 
ip address add dev Carn-eth1 fd00:300:3:f02::4/64 

ip address add dev Carn-lan0 fd00:200:3:f040::4/64 
ip address add dev Carn-lan0 fd00:300:3:f040::4/64 


bird6 -s /tmp/Carn_bird.ctl -P /tmp/Carn_bird.pid 

snmpd &> /dev/null
