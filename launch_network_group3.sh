#!/bin/bash

# Cleanup
sudo ./cleanup.sh

#creation of routers directories
#logs
mkdir -p group3_cfg/Halles/log
mkdir -p group3_cfg/Pythagore/log
#bird
mkdir -p group3_cfg/Halles/bird
mkdir -p group3_cfg/Pythagore/bird

sudo touch group3_cfg/Halles/log/bird_log
sudo touch group3_cfg/Halles/log/backup_link_log
sudo touch group3_cfg/Pythagore/log/bird_log
sudo touch group3_cfg/Pythagore/log/backup_link_log



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
