#!/bin/bash 

# This file has been generated automatically, see router_config_creation.py 
ip link set dev belneta up 
ip address add dev belneta fd00:300::3/48  

ip link set dev Pyth-eth0 up 
ip address add dev Pyth-eth0 fd00:200:3:0::2/64 
ip address add dev Pyth-eth0 fd00:300:3:0::2/64 
ip link set dev Pyth-eth1 up 
ip address add dev Pyth-eth1 fd00:200:3:2::2/64 
ip address add dev Pyth-eth1 fd00:300:3:2::2/64 
ip link set dev Pyth-eth2 up 
ip address add dev Pyth-eth2 fd00:200:3:1::2/64 
ip address add dev Pyth-eth2 fd00:300:3:1::2/64 

ip link set dev Pyth-lan1-Mon up 
ip address add dev Pyth-lan1-Mon fd00:200:3:ffff::2/64 
ip address add dev Pyth-lan1-Mon fd00:300:3:ffff::2/64 

bird6 -s /tmp/Pyth_bird.ctl -P /tmp/Pyth_bird.pid 
