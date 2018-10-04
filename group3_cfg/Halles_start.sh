#!/bin/bash

ip link set dev belnetb up
ifconfig belneta inet6 add fd00:200::3/48


ip link set dev Halles-eth0 up
ifconfig Halles-eth0 inet6 add fd00:200:3:6::1/64
ifconfig Halles-eth0 inet6 add fd00:300:3:6::1/64
ip link set dev Halles-eth1 up
ifconfig Halles-eth1 inet6 add fd00:200:3:0::1/64
ifconfig Halles-eth1 inet6 add fd00:300:3:0::1/64
puppet apply --verbose --parser future --hiera_config=/etc/puppet/hiera.yaml /etc/puppet/site.pp --modulepath=/puppetmodules
