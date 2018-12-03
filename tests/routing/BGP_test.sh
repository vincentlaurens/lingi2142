#!/usr/bin/env bash

#!/bin/bash

#Ping if every router ping provider

# 1 ping with 2 sec timeout
echo "Test can take few minutes"
sudo ip netns exec Pyth ping6 -c 15 -W 1 fd00:200::b > /dev/null
   if [ $? != 0 ]
   then
        echo "Pyth failed"
   else echo "Pyth succeded"
   fi

sudo ip netns exec Pyth ping6 -c 2 -W 1 fd00:300::b > /dev/null
   if [ $? != 0 ]
   then
        echo "Pyth failed"
   else echo "Pyth succeded"
   fi

sudo ip netns exec Hall ping6 -c 2 -W 1 fd00:200::b > /dev/null
   if [ $? != 0 ]
   then
        echo "Hall failed"
   else echo "Hall succeded"
   fi
sudo ip netns exec Hall ping6 -c 2 -W 1 fd00:300::b > /dev/null
   if [ $? != 0 ]
   then
        echo "Hall failed"
   else echo "Hall succeded"
   fi
exit
