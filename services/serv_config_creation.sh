#!/bin/bash

# This script is called from parent folder (cd ./..)

# Create directory
sudo mkdir -p ./group3_cfg/

# Copy configuration
sudo cp ./services/Serv_start.sh ./group3_cfg/Serv_start.sh
sudo  mkdir -p ./group3_cfg/Serv
