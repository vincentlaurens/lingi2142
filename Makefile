all:
	sudo ./launch_network_group3.sh

clean:
	sudo rm -r group3_cfg/*

connect:
	sudo ./connect_to.sh group3_cfg ${namespace}

restartFirewall:
	sudo sh iptables/restartFirewall.sh

runTestRouting:
	sudo sh tests/runtest.sh

runTestFirewall:
	sudo sh tests/firewall/firewall_test.sh



Mon:
	sudo ./connect_to.sh group3_cfg Mon

Pyth:
	sudo ./connect_to.sh group3_cfg Pyth

Hall:
	sudo ./connect_to.sh group3_cfg Hall

rsync:
	rsync -r /vagrant/* /home/vagrant/test/group3/lingi2142/

