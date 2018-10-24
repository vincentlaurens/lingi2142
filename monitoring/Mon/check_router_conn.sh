#!/bin/bash

LOG_FILE="/etc/log/conn_status_log"
exec &>> $LOG_FILE

declare -A IP
IP+=( ["Halles-eth0"]="fd00:300:3:6::1" \
      ["Halles-eth1"]="fd00:300:3:3::1" \
      ["belneta"]="fd00:200::3"         \
      ["Pyth-eth0"]="fd00:300:3:3::2"   \
      ["Pyth-eth1"]="fd00:300:3:2::2"   \
      ["Pyth-eth2"]="fd00:300:3:1::2"   \
      ["belneta"]="fd00:300::3"         \
      ["Stev-eth0"]="fd00:300:3:3::3"   \
      ["Stev-eth1"]="fd00:300:3:1::3"   \
      ["Carn-eth0"]="fd00:300:3:4::4"   \
      ["Carn-eth1"]="fd00:300:3:2::4"   \
      ["Carn-eth2"]="fd00:300:3:3::4"   \
      ["Minch-eth0"]="fd00:300:3:5::5"  \
      ["Minch-eth1"]="fd00:300:3:6::5"  \
      ["SH1C-eth0"]="fd00:300:3:5::6"   \
      ["SH1C-eth1"]="fd00:300:3:6::6"   )

# Wait for start of the network
sleep 30

for interface in "${!IP[@]}"
do
    ping6 -c 1 -W 1 ${IP[$interface]} #> /dev/null

    if [ $? != 0 ]
    then
        echo "[ERROR] Failed to ping ${interface}, ip: ${IP[$interface]}" >> LOG_FILE
    fi
done

exit