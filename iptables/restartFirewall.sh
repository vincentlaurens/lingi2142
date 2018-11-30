#!/bin/bash

echo "Starting the firewalls on all routers ..."

sudo ip netns exec "Hall" ./iptables/Hall.sh

sudo ip netns exec "Pyth" ./iptables/Pyth.sh

sudo ip netns exec "Stev" ./iptables/Stev.sh

sudo ip netns exec "SH1C" ./iptables/SH1C.sh

sudo ip netns exec "Carn" ./iptables/Carn.sh

sudo ip netns exec "Mich" ./iptables/Mich.sh

echo "All the firewalls have been set !"

exit 0