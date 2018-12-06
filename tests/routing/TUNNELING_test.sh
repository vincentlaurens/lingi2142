#!/usr/bin/env bash

echo "[Test TUNNEL]"

echo "[Test TUNNEL] Test can take few minutes"
echo "[Test TUNNEL] On Hall see trace on /tmp/tunneltoHall.pcap"
echo "[Test TUNNEL] Open it with command: sudo tcpdump -ttttnnr /tmp/tunneltoHall.pcap"
sudo ip netns exec Hall sudo tcpdump -ni any -w /tmp/tunneltoHall.pcap -ttt &
sleep 1
echo "[Test TUNNEL] ping6 from Pyth to Hall provider"
sudo ip netns exec Pyth ping6 -c 15 -W 1 fd00:200::b > /dev/null


echo "[Test TUNNEL] Test can take few minutes"
echo "[Test TUNNEL] On Hall see trace on /tmp/tunneltoPyth.pcap"
echo "[Test TUNNEL] Open it with command: /tmp/tunneltoPyth.pcap"
sudo ip netns exec Pyth sudo tcpdump -ni any -w /tmp/tunneltoPyth.pcap -ttt &
seep1

echo "[Test TUNNEL] ping6 from Pyth to Hall provider"
sudo ip netns exec Hall ping6 -c 15 -W 1 fd00:300::b > /dev/null

sleep 1
pkill tcpdump

echo "[Test TUNNEL] End of script"
