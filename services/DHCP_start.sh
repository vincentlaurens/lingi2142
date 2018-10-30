#!/bin/bash

# Interfaces
#DHCP server
ip address add dev Dhcp-eth0 fd00:200:3:1000::547/64
ip address add dev Dhcp-eth0 fd00:300:3:1000::547/64
# Gateway
ip -6 route add ::/0 via fd00:200:3:1000::1/64 #address of Hall