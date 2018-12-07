#!/bin/bash

ROOT='/vagrant'
sudo mkdir -p $ROOT/services/DNS/bind/named_zones/zones
sudo bash $ROOT/services/DNS/bind/src/dns_conf_creat.sh
sudo mkdir -p $ROOT/group3_cfg/DNS/bind/
sudo mkdir -p $ROOT/group3_cfg/DNS/bind/zones

#sudo mkdir -p /var/log/bind/bind/dns.log
#sudo cp $ROOT/services/DNS/bind/src/utils_dns.py $ROOT/group3_cfg/DNS/bind/
sudo cp $ROOT/services/DNS/bind/named_zones/zones/* $ROOT/group3_cfg/DNS/bind/zones
sudo cp $ROOT/services/DNS/bind/named_zones/named.conf* $ROOT/group3_cfg/DNS/bind/

