#!/bin/bash 

# This file has been generated automatically, see service_config_creation.py for details. 

ip address add dev Ha2-eth0 fd00:200:3:f025::2/64

ip address add dev Ha2-eth0 fd00:300:3:f025::2/64

ip -6 route add ::/0 via fd00:200:3:f025::1 
ip -6 route add fd00:300:3:f025::1 dev Ha2-eth0 

