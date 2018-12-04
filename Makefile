all:
	sudo ./launch_network_group3.sh

clean:
	sudo rm -r group3_cfg/*

connect:
	sudo ./connect_to.sh group3_cfg ${ns}

runTestRouting:
	sudo ./tests/runtest.sh

runTestFirewall_choose_port:
	sudo ./tests/firewall/firewall_choose_port_test.sh ${ns} ${ip} ${port}

runTestFirewall_choose:
	sudo ./tests/firewall/firewall_choose_test.sh ${ns} ${ip}

runTestFirewall_firewall_border:
	sudo ./tests/firewall/firewall_test.sh

rsync:
	rsync -r /vagrant/* /home/vagrant/test/group3/lingi2142/


restartFirewall:
	sudo ./iptables/restartFirewall.sh