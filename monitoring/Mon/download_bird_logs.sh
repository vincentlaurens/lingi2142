#!/bin/bash

mkdir -p /etc/log/bird_logs

ROUTERS_TO_CHECK=("Hall" "Pyth" "Stev" "Carn" "Mich" "SH1C")

while true
do
    for ROUTER in "${ROUTERS_TO_CHECK[@]}";
    do
        cp ./group3_cfg/${ROUTER}/log/bird_log /etc/log/bird_logs/${ROUTER}_bird_log
    done

    sleep 10
done

exit