#!/bin/bash

ROOT='/home/vagrant/test/group3/lingi2142'
sudo mkdir -p $ROOT/services/DNS/bind/named_zones/zones
sudo bash $ROOT/services/DNS/bind/src/dns_conf_creat.sh
sudo mkdir -p $ROOT/group3_cfg/DNS1/bind/
sudo mkdir -p $ROOT/group3_cfg/DNS1/bind/zones


sudo mkdir -p $ROOT/services/DNS/bind2/named_zones/zones
sudo bash $ROOT/services/DNS/bind2/src/dns_conf_creat.sh
sudo mkdir -p $ROOT/group3_cfg/DNS2/bind/
sudo mkdir -p $ROOT/group3_cfg/DNS2/bind/zones

#sudo mkdir -p /var/log/bind/bind/dns.log
#sudo cp $ROOT/services/DNS/bind/src/utils_dns.py $ROOT/group3_cfg/DNS/bind/
sudo cp $ROOT/services/DNS/bind/named_zones/zones/* $ROOT/group3_cfg/DNS/bind/zones
sudo cp $ROOT/services/DNS/bind/named_zones/named.conf* $ROOT/group3_cfg/DNS/bind/

sudo cp $ROOT/services/DNS/bind2/named_zones/zones/* $ROOT/group3_cfg/DNS2/bind/zones
sudo cp $ROOT/services/DNS/bind2/named_zones/named.conf* $ROOT/group3_cfg/DNS2/bind/
