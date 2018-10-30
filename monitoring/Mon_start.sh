#!/bin/bash

# Interfaces
#ip link set dev Mon-eth0 up
ip address add dev Mon-eth0 fd00:200:3:ffff::1/64
ip address add dev Mon-eth0 fd00:300:3:ffff::1/64

# Gateway
ip -6 route add ::/0 via fd00:200:3:ffff::2 #address of pyth
ip -6 route add ::/0 via fd00:300:3:ffff::2

# Scripts
/etc/check_isp_status.sh &
/etc/check_dns_status.sh &
/etc/check_router_conn.sh &
/etc/download_bird_logs.sh
