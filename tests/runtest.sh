#!/usr/bin/env bash

sudo chmod 755 ./routing/BGP_test.sh
sudo chmod 755 ./routing/OSPF_test.sh
sudo sh ./routing/BGP_test.sh
sleep 10
sudo sh ./routing/OSPF_test.sh
sleep 10
