#!/bin/bash

#Ping if every router ping provider

# 1 ping with 2 sec timeout
echo "[TEST OSPF: It can take few minutes. Be patient]"
sudo ip netns exec Mich ping6 -c 15 -W 1 fd00:200::b > /dev/null # Will return '0' if ping was successful
   if [ $? != 0 ]
   then
        echo "Mich failed"
   else echo "Mich succeded"
   fi

sudo ip netns exec Mich ping6 -c 2 -W 1 fd00:300::b > /dev/null # Will return '0' if ping was successful
   if [ $? != 0 ]
   then
        echo "Mich failed"
   else echo "Mich succeded"
   fi

sudo ip netns exec Carn ping6 -c 2 -W 1 fd00:200::b > /dev/null # Will ret$
   if [ $? != 0 ]
   then
        echo "Carn failed"
   else echo "Carn succeded"
   fi
sudo ip netns exec Carn ping6 -c 2 -W 1 fd00:300::b > /dev/null # Will ret$
   if [ $? != 0 ]
   then
        echo "Carn failed"
   else echo "Carn succeded"
   fi

sudo ip netns exec SH1C ping6 -c 2 -W 1 fd00:200::b > /dev/null # Will ret$
   if [ $? != 0 ]
   then
        echo "SH1C failed"
   else echo "SH1C succeded"
   fi
sudo ip netns exec SH1C ping6 -c 2 -W 1 fd00:300::b > /dev/null # Will ret$
   if [ $? != 0 ]
   then
        echo "SH1C failed"
   else echo "SH1C succeded"
   fi
exit
