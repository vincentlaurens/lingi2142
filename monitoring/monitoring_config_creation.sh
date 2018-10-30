#!/bin/bash

# This script is called from parent folder (cd ./..)

# Create directory
sudo mkdir -p ./group3_cfg/

# Copy configuration
sudo cp ./monitoring/Mon_start.sh ./group3_cfg/Mon_start.sh
sudo cp -R ./monitoring/Mon ./group3_cfg/