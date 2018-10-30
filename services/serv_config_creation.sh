#!/bin/bash

# This script is called from parent folder (cd ./..)

# Create directory
sudo mkdir -p ./group3_cfg/

# Copy configuration
sudo cp ./services/Dns_start.sh ./group3_cfg/Dns_start.sh
sudo  mkdir -p ./group3_cfg/Dns
sudo cp ./services/Dhcp_start.sh ./group3_cfg/Dhcp_start.sh
sudo  mkdir -p ./group3_cfg/Dhcp


