#!/bin/bash

ROOT='/home/vagrant/lingi2142'
sudo mkdir -p $ROOT/netwok_server/bind/named_zones/zones
sudo bash $ROOT/netwok_server/bind/src/dns_conf_creat.sh

sudo mkdir -p $ROOT/group3_cfg/NS1/bind/
sudo mkdir -p $ROOT/group3_cfg/NS1/bind/zones
sudo mkdir -p /var/log/bind/bind/dns.log
sudo cp $ROOT/netwok_server/bind/src/utils_dns.py $ROOT/group3_cfg/NS1/bind/
sudo cp $ROOT/netwok_server/bind/named_zones/zones/* $ROOT/group3_cfg/NS1/bind/zones
sudo cp $ROOT/netwok_server/bind/named_zones/named.conf* $ROOT/group3_cfg/NS1/bind/
sudo cp $ROOT/netwok_server/bind/src/update_dns.py $ROOT/group3_cfg/NS1/bind/
chmod +x $ROOT/group3_cfg/NS1/bind/update_dns.py