#!/usr/bin/env bash

echo "[Test TUNNEL]"

echo "[Test TUNNEL] Test can take few minutes"
echo "[Test TUNNEL] On Hall see trace on /tmp/tunnel.pcap"
echo "[Test TUNNEL] Open it with wireshark"
sudo ip netns exec Hall tcpdump -ni any -w /tmp/tunneltoHall.pcap

echo "[Test TUNNEL] ping6 from Pyth to Hall provider"
sudo ip netns exec Pyth ping6 -c 15 -W 1 fd00:200::b > /dev/null


echo "[Test TUNNEL] Test can take few minutes"
echo "[Test TUNNEL] On Hall see trace on /tmp/tunnel.pcap"
echo "[Test TUNNEL] Open it with wireshark"
sudo ip netns exec Pyth tcpdump -ni any -w /tmp/tunneltoPyth.pcap

echo "[Test TUNNEL] ping6 from Pyth to Hall provider"
sudo ip netns exec Hall ping6 -c 15 -W 1 fd00:300::b > /dev/null

echo "[Test TUNNEL] End of script"