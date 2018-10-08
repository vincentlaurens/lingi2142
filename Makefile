all:
	sudo ./launch_network_group3.sh

clean:
	
	sudo rm -r group3_cfg/*

Halles:
	sudo ./connect_to.sh group3_cfg Halles
Pyth:
	sudo ./connect_to.sh group3_cfg Pyth
Stev:
	sudo ./connect_to.sh group3_cfg Stev
