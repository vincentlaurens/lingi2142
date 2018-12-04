#!/bin/bash


apt-get -y -qq --force-yes update
apt-get -y -qq --force-yes install build-essential checkinstall
#if !which cmake; then
#	wget http://www.cmake.org/files/v3.2/cmake-3.2.2.tar.gz
#	tar xf cmake-3.2.2.tar.gz
#	cd cmake-3.2.2
#	./configure
#	make
#	checkinstall -y
#	cd ..
#fi
apt-get -y -qq --force-yes update

apt-get -y -qq --force-yes install git bash lib32z1 vim-nox tcpdump nano\
								   bird6 quagga inotify-tools\
								   iperf bind9 bind9-doc bind9utils \
								   nmap python3
								   #radvd isc-dhcp-server isc-dhcp-client\

# "isc-dhcp-relay" if this package is in "apt-get install", the "vagrant up" will freeze

# dependencies for puppet
# apt-get -y -qq --force-yes install ruby ruby-dev libboost-all-dev gettext curl libcurl4-openssl-dev libyaml-cpp-dev
apt-get -y -qq --force-yes install puppet # TODO Get more recent version of puppet
#gem install puppet -f

# Monitoring
apt-get -y -qq --force-yes install snmp snmpd python-pip software-properties-common
pip install pysnmp
apt-add-repository non-free
apt-get -y -qq --force-yes update
apt-get -y -qq --force-yes install snmp-mibs-downloader
download-mibs

#Wireshark
apt-get  -qq --force-yes install build-essential checkinstall libcurl4-openssl-dev bison flex qt5-default qttools5-dev libssl-dev libgtk-3-dev libpcap-d
add-apt-repository  -qq --force-yes ppa:wireshark-dev/stable
apt-get  -qq --force-yes update
apt-get  -qq --force-yes install wireshark

update-rc.d quagga disable &> /dev/null || true
update-rc.d bird disable &> /dev/null || true
update-rc.d bird6 disable &> /dev/null || true

service quagga stop
service bird stop
service bird6 stop
service bind9 stop

(cd /sbin && ln -s /usr/lib/quagga/* .)

su vagrant -c 'cd && mkdir -p /home/vagrant/test/group3/lingi2142 && cp -r /vagrant/* "$_"'
