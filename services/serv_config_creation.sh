#!/bin/bash

# This script is called from parent folder (cd ./..)

# Create directory
sudo mkdir -p ./group3_cfg/

# Copy configuration
sudo cp ./services/DNS_start.sh ./group3_cfg/DNS_start.sh
sudo cp -R ./services/DNS ./group3_cfg/
sudo cp ./services/DHCP_start.sh ./group3_cfg/DHCP_start.sh
sudo cp -R ./services/DHCP ./group3_cfg/