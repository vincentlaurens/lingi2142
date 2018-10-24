#!/bin/bash

LOG_FILE="/etc/log/dns_status_log"
exec &>> $LOG_FILE

declare -A DNS
DNS+=( ["ns1"]="fd00:300:3:1000::1" ["ns2"]="fd00:300:3:2000::1" )

# Wait for start of the network
sleep 15

while true
do
    # Check DNSs
    for DNS_NAME in "${!DNS[@]}";
    do
        ping6 -c 3 ${DNS[$DNS_NAME]} > /dev/null

        if [ $? != 0 ] # not reachable
        then
            echo "[WARN] (`date`) $DNS_NAME is unreachable at ${DNS[$DNS_NAME]} from Mon" >> $LOG_FILE
        else
            echo "[OK] (`date`) $DNS_NAME is reachable" >> $LOG_FILE
        fi
    done

    sleep 8
done

exit
