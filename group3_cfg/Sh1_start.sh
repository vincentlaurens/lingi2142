#!/bin/bash 

# This file has been generated automatically, see service_config_creation.py for details. 

ip address add dev Sh1-eth0 fd00:200:3:f034::1/64

ip address add dev Sh1-eth0 fd00:300:3:f034::1/64

ip -6 route add ::/0 via fd00:200:3:f034::6 
ip -6 route add fd00:300:3:f034::6 dev Sh1-eth0 

