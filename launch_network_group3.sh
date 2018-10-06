#!/bin/bash

# Cleanup
sudo ./cleanup.sh
#mkdir -p project_cfg/MONI/log
mkdir -p project_cfg/Halles/log
#mkdir -p project_cfg/MICH/log
mkdir -p project_cfg/Pythagore/log
#mkdir -p project_cfg/STEV/log
#mkdir -p project_cfg/SH1C/log
#mkdir -p project_cfg/CARN/log
#mkdir -p /var/cache/bind/ns1
#mkdir -p /var/cache/bind/ns2


#sudo echo > project_cfg/MONIT/log/services_status_log
#sudo echo > project_cfg/MONIT/log/isp_status_log
sudo echo > project_cfg/Halles/log/bird_log
sudo echo > project_cfg/Halles/log/backup_link_log
sudo echo > project_cfg/Pythagore/log/bird_log
sudo echo > project_cfg/Pythagore/log/backup_link_log
#sudo echo > project_cfg/STEV/log/bird_log
#sudo echo > project_cfg/CARN/log/bird_log
#sudo echo > project_cfg/MICH/log/bird_log
#sudo echo > project_cfg/SH1C/log/bird_log

# Configuration files creation
sudo ./router_config_creation.py
#sudo ./service_config_creation.py
#sudo ./host_config_creation.py
#sudo ./end_user_management/deploy_end_user_management.sh

# Network creation
sudo ./create_network.sh group3_topo

# QoS
#sudo ./qos/deploy_qos.sh

# Webservice
#sudo ./start_haproxy.sh
