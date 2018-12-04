#!/usr/bin/env bash


echo "param1 $1 : fill with a router namespace"
echo "param2 $2 :fill with a ip address interface of chosen router"

 sudo ip netns exec "$1" nmap -6 -sU -sT -p0-1000  $2 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "scan terminate succefully"
   fi