#!/bin/bash 

# This file has been generated automatically, see service_config_creation.py for details. 

ip address add dev Mon-eth0 fd00:200:3:f02f::1/64
ip address add dev Mon-eth0 fd00:300:3:f02f::1/64

ip -6 route add ::/0 via fd00:200:3:f02f::2 
ip -6 route add fd00:300:3:f02f::2 dev Mon-eth0 

/etc/check_isp_status.sh &
/etc/check_dns_status.sh &
/etc/check_router_conn.sh &
/etc/download_bird_logs.sh &
python /etc/snmp.py &
