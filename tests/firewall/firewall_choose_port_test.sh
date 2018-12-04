#!/usr/bin/env bash


echo "param1 $1: fill with a router namespace"
echo "param2 $2: fill with a ip address interface of chosen router"
echo "param3 $3 : choose a port to scan"

 sudo ip netns exec "$1" nmap -6 -p $3 $2 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port $3 open or filtered"
   fi