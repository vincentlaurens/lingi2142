#!/bin/bash

# Cleanup
sudo ./cleanup.sh

#creation of routers directories
#logs
mkdir -p group3_cfg/Halles/log
mkdir -p group3_cfg/Pyth/log
mkdir -p group3_cfg/Stev/log
mkdir -p group3_cfg/SH1C/log
mkdir -p group3_cfg/Carn/log
mkdir -p group3_cfg/Mich/log

#iptables

mkdir -p iptables

sudo touch iptables/launchfirewall.sh
sudo touch iptables/Halles.sh
sudo touch iptables/Pyth.sh
sudo touch iptables/Stev.sh
sudo touch iptables/SH1C.sh
sudo touch iptables/Carn.sh
sudo touch iptables/Mich.sh

sudo touch group3_cfg/Halles/log/iptables_log
sudo touch group3_cfg/Pyth/log/iptables_log
sudo touch group3_cfg/SH1C/log/iptables_log
sudo touch group3_cfg/Carn/log/iptables_log
sudo touch group3_cfg/Mich/log/iptables_log

#bird
mkdir -p group3_cfg/Halles/bird
mkdir -p group3_cfg/Pyth/bird
mkdir -p group3_cfg/Stev/bird
mkdir -p group3_cfg/Carn/bird
mkdir -p group3_cfg/Mich/bird
mkdir -p group3_cfg/SH1C/bird

sudo touch group3_cfg/Halles/log/bird_log
sudo touch group3_cfg/Halles/log/backup_link_log
sudo touch group3_cfg/Pyth/log/bird_log
sudo touch group3_cfg/Pyth/log/backup_link_log
sudo touch group3_cfg/Stev/log/bird_log
sudo touch group3_cfg/SH1C/log/bird_log
sudo touch group3_cfg/Carn/log/bird_log
sudo touch group3_cfg/Mich/log/bird_log



# Configuration files creation
sudo python3 router_config_creation.py
sudo python3 firewall_config_creation.py
sudo ./monitoring/monitoring_config_creation.sh
#sudo ./service_config_creation.py
#sudo ./host_config_creation.py
#sudo ./end_user_management/deploy_end_user_management.sh

# Network creation
sudo ./create_network.sh group3_topo

#FireWall
sudo sh iptables/launchfirewall.sh

# QoS
#sudo ./qos/deploy_qos.sh

# Webservice
#sudo ./start_haproxy.sh

