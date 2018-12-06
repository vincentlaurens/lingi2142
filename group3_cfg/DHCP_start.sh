#!/bin/bash 

# This file has been generated automatically, see service_config_creation.py for details. 

ip address add dev DHCP-eth0 fd00:200:3:f061::547/64
ip address add dev DHCP-eth0 fd00:300:3:f061::547/64

ip -6 route add ::/0 via fd00:200:3:f061::6 
ip -6 route add fd00:300:3:f061::6 dev DHCP-eth0 

dhcpd -q -6 -f -cf /etc/dhcp/dhcpd6.conf -pf /var/run/dhcpd1.pid -tf /var/log/dhcpd/dhcpd1.log  -lf /etc/dhcp/dhcpd6.leases
