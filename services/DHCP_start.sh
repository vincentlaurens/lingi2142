#!/bin/bash

# Interfaces
#DHCP server
#223 hexa = 547 dec qui est le port DHCP
ip address add dev DHCP-eth0 fd00:200:3:1000::223/64
ip address add dev DHCP-eth0 fd00:300:3:1000::223/64
# Gateway
ip -6 route add ::/0 via fd00:200:3:1000::1 #address of Hall