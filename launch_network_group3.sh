#!/bin/bash

# Cleanup
sudo ./cleanup.sh
sleep 5

#creation of routers directories
#logs
mkdir -p group3_cfg/Hall/log
mkdir -p group3_cfg/Pyth/log
mkdir -p group3_cfg/Stev/log
mkdir -p group3_cfg/SH1C/log
mkdir -p group3_cfg/Carn/log
mkdir -p group3_cfg/Mich/log

#iptables

mkdir -p iptables

sudo touch iptables/restartFirewall.sh
sudo touch iptables/Hall.sh
sudo touch iptables/Pyth.sh
sudo touch iptables/Stev.sh
sudo touch iptables/SH1C.sh
sudo touch iptables/Carn.sh
sudo touch iptables/Mich.sh

sudo touch group3_cfg/Hall/log/iptables_log
sudo touch group3_cfg/Pyth/log/iptables_log
sudo touch group3_cfg/SH1C/log/iptables_log
sudo touch group3_cfg/Carn/log/iptables_log
sudo touch group3_cfg/Mich/log/iptables_log

#bird
mkdir -p group3_cfg/Hall/bird
mkdir -p group3_cfg/Pyth/bird
mkdir -p group3_cfg/Stev/bird
mkdir -p group3_cfg/Carn/bird
mkdir -p group3_cfg/Mich/bird
mkdir -p group3_cfg/SH1C/bird

sudo touch group3_cfg/Hall/log/bird_log
sudo touch group3_cfg/Hall/log/backup_link_log
sudo touch group3_cfg/Pyth/log/bird_log
sudo touch group3_cfg/Pyth/log/backup_link_log
sudo touch group3_cfg/Stev/log/bird_log
sudo touch group3_cfg/SH1C/log/bird_log
sudo touch group3_cfg/Carn/log/bird_log
sudo touch group3_cfg/Mich/log/bird_log

# Monitoring
sudo cp -R ./monitoring/Mon ./group3_cfg/
sudo cp -R ./monitoring/snmp ./group3_cfg/Pyth/

# Configuration files creation
sudo python3 firewall_config_creation.py
sudo python3 router_config_creation.py
sudo python3 service_config_creation.py
sudo python3 host_config_creation.py

#sudo chmod 755 ./services/deploy_service.sh
#sudo sh services/deploy_service.sh


# Network creation
sudo ./create_network.sh group3_topo


