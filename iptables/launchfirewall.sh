#!/bin/bash

echo "Starting the firewalls on all routers ..."

sudo ip netns exec "Halles" ./iptables/Halles.sh

sudo ip netns exec "Pyth" ./Pyth.sh

sudo ip netns exec "Stev" ./Stev.sh

sudo ip netns exec "SH1C" ./SH1C.sh

sudo ip netns exec "Carn" ./Carno.sh

sudo ip netns exec "Mich" ./Mich.sh

echo "All the firewalls have been set !"

exit 0