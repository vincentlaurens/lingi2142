#!/bin/bash 

# This file has been generated automatically, see service_config_creation.py for details. 

ip address add dev Sh2-eth0 fd00:200:3:f035::2/64

ip address add dev Sh2-eth0 fd00:300:3:f035::2/64

ip -6 route add ::/0 via fd00:200:3:f035::6 
ip -6 route add fd00:300:3:f035::6 dev Sh2-eth0 

