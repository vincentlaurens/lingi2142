#!/bin/bash

ROOT='/vagrant'
sudo mkdir -p $ROOT/services/DNS/bind2/named_zones/zones
sudo bash $ROOT/services/DNS/bind2/src/dns_conf_creat.sh
sudo mkdir -p $ROOT/group3_cfg/DNS2/bind/
sudo mkdir -p $ROOT/group3_cfg/DNS2/bind/zones

sudo cp $ROOT/services/DNS/bind2/named_zones/zones/* $ROOT/group3_cfg/DNS2/bind/zones
sudo cp $ROOT/services/DNS/bind2/named_zones/named.conf* $ROOT/group3_cfg/DNS2/bind/