
all:
	sudo ./launch_network_group3.sh

clean:
	sudo rm -r group3_cfg/*
connect:
	sudo ./connect_to.sh group3_cfg ${namespace}
restartFirewall:
	sudo sh iptables/restartFirewall.sh

Hall:
	sudo ./connect_to.sh group3_cfg Hall
Pyth:
	sudo ./connect_to.sh group3_cfg Pyth
Stev:
	sudo ./connect_to.sh group3_cfg Stev
Carn:
	sudo ./connect_to.sh group3_cfg Carn
Mich:
	sudo ./connect_to.sh group3_cfg Mich
SH1C:
	sudo ./connect_to.sh group3_cfg SH1C
Mon:
	sudo ./connect_to.sh group3_cfg Mon
DNS:
	sudo ./connect_to.sh group3_cfg DNS
DHCP:
	sudo ./connect_to.sh group3_cfg DHCP

