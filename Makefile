
all:
	sudo ./launch_network_group3.sh

clean:
	sudo rm -r group3_cfg/*

connect:
	sudo ./connect_to.sh group3_cfg ${namespace}

restartFirewall:
	sudo sh iptables/restartFirewall.sh


