#!/bin/bash 

# This file has been generated automatically, see service_config_creation.py for details. 

ip address add dev DNS2-eth0 fd00:200:3:f032::53/64
ip address add dev DNS2-eth0 fd00:300:3:f032::53/64

ip -6 route add ::/0 via fd00:200:3:f032::3 
ip -6 route add fd00:300:3:f032::3 dev DNS2-eth0 

named -6 -c /etc/bind/named1.conf 

