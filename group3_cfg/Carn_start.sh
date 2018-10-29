#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip link set dev Carn-eth0 up 
ip address add dev Carn-eth0 fd00:200:3:4::4/64 
ip address add dev Carn-eth0 fd00:300:3:4::4/64 
ip link set dev Carn-eth1 up 
ip address add dev Carn-eth1 fd00:200:3:2::4/64 
ip address add dev Carn-eth1 fd00:300:3:2::4/64 
ip link set dev Carn-eth2 up 
ip address add dev Carn-eth2 fd00:200:3:3::4/64 
ip address add dev Carn-eth2 fd00:300:3:3::4/64 

ip link set dev Carn-lan0-Stud up 
ip address add dev Carn-lan0-Stud fd00:200:3:040::4/64 
ip address add dev Carn-lan0-Stud fd00:300:3:040::4/64 
ip link set dev Carn-lan1-Staff: up 
ip address add dev Carn-lan1-Staff: fd00:200:3:041::4/64 
ip address add dev Carn-lan1-Staff: fd00:300:3:041::4/64 

bird6 -s /tmp/Carn_bird.ctl -P /tmp/Carn_bird.pid 
