#!/bin/bash

LOG_FILE="/etc/log/isp_status_log"
exec &>> $LOG_FILE

ROUTERS_TO_CHECK=("Halles" "Pyth")
BGP=("provider200" "provider300")

# Wait for start of the network
sleep 15

while true
do
	# Check connectivity with ISP on each router
	for (( i =0 ; i < ${#ROUTERS_TO_CHECK[@]}; i++ ));
	do
		status=$(birdc6 -s /tmp/${ROUTERS_TO_CHECK[$i]}_bird.ctl "show protocol ${BGP[$i]}" | grep ${BGP[$i]} | awk {'print $6'})

		# If ISP is reachable
		if [ "$status" = "Established"  ]
		then
			echo "[OK] (`date`) ${BGP[$i]}, Status of BGP peering is: ${status}." >> $LOG_FILE
		else
			echo "[WARN] (`date`) ${BGP[$i]}, Status of BGP peering is: ${status}." >> $LOG_FILE
		fi
	done

	sleep 8
done

exit
