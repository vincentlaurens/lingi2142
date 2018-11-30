#!/usr/bin/env bash



sudo nmap -6 -sU -sT -p0-1000  fd00:200::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "scan terminate succefully"
   fi

sudo nmap -6 -sU -sT -p0-1000  fd00:300::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "scan terminate succefully"
   fi


sudo nmap -6 -p 179  fd00:200::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 179 open (filtered)"
   fi

sudo nmap -6 -p 179  fd00:300::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 179 open (filtered)"
   fi

sudo nmap -6 -p 89  fd00:200::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 89 filtered ok"
   fi

sudo nmap -6 -p 89  fd00:300::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 89 filtered ok"
   fi

sudo nmap -6 -p 161  fd00:200::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 161 filtered ok"
   fi

sudo nmap -6 -p 161  fd00:300::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 161 filtered ok"
   fi

sudo nmap -6 -p 162  fd00:200::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 162 filtered ok"
   fi

sudo nmap -6 -p 162  fd00:300::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 162 filtered ok"
   fi

sudo nmap -6 -p 546  fd00:200::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 546 filtered ok"
   fi

sudo nmap -6 -p 546  fd00:300::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 546 filtered ok"
   fi

sudo nmap -6 -p 547  fd00:200::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 547 filtered ok"
   fi

sudo nmap -6 -p 547  fd00:300::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 547 filtered ok"
   fi


sudo nmap -6 -p 23  fd00:200::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 547 filtered ok"
   fi

sudo nmap -6 -p 23  fd00:300::3 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 547 filtered ok"
   fi

sudo nmap -6 -p 23  fd00:300:3:f00::1 > /dev/null
   if [ $? != 0 ]
   then
        echo "port failed"
   else echo "port 23 filtered ok"
   fi