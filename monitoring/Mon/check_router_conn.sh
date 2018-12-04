#!/bin/bash

LOG_FILE="/etc/log/conn_status_log"
exec &>> $LOG_FILE

declare -A IP
IP+=( ["Hall-eth0"]="fd00:300:3:f06::1" \
      ["Hall-eth1"]="fd00:300:3:f00::1" \
      ["belnetb"]="fd00:200::3"         \
      ["Pyth-eth0"]="fd00:300:3:f00::2"   \
      ["Pyth-eth1"]="fd00:300:3:f02::2"   \
      ["Pyth-eth2"]="fd00:300:3:f01::2"   \
      ["belneta"]="fd00:300::3"         \
      ["Stev-eth0"]="fd00:300:3:f03::3"   \
      ["Stev-eth1"]="fd00:300:3:f01::3"   \
      ["Carn-eth0"]="fd00:300:3:f04::4"   \
      ["Carn-eth1"]="fd00:300:3:f02::4"   \
      ["Carn-eth2"]="fd00:300:3:f03::4"   \
      ["Minch-eth0"]="fd00:300:3:f05::5"  \
      ["Minch-eth1"]="fd00:300:3:f04::5"  \
      ["SH1C-eth0"]="fd00:300:3:f05::6"   \
      ["SH1C-eth1"]="fd00:300:3:f06::6"   )

while true
do
	for interface in "${!IP[@]}"
	do
		ping6 -c 1 -W 1 ${IP[$interface]} > /dev/null

		if [ $? != 0 ]
		then
			echo "[ERROR] (`date`) Failed to ping ${interface}, ip: ${IP[$interface]}" >> $LOG_FILE
		fi
	done

	sleep 5
done

exit