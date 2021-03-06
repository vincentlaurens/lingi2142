# lingi2142

This repository contains:

  * the set of scripts to provision VMs, build a virtual exchange point and
    run a virtual campus networks on a VM for the course
    [LINGI2142 ](https://moodleucl.uclouvain.be/course/view.php?id=9209) at 
    [UCLouvain](https://uclouvain.be) in order to emulate campus networks and
    interconnect them.
  * Some of the student's implementation, showcasing various aspects of the 
    configuration and management of an IPv6-only multihomed network using
    provider-assigned prefixes, in the [student_projects](student_projects)
    folder. An overview of these project, as well as a feature highlight is
    available in the [README file](student_projects/README.md).
  * [host](host) defines the script to hosts a remote set of VMs for each
      group.

# Virtual machine

A sample virtual machine definition to run the script is provided and managed
using [Vagrant](https://www.vagrantup.com), using a
[VirtualBox](https://www.virtualbox.org) provider. 

You *need* to install *both* of these softwares on your machine in order to
run an emulated network.

## Commands summary

  * Caution !!! Modify the PATH variable of [constant.py](constant.py)  by project working Directory ("/vagrant/")

  * [./build_vm.sh](build_vm.sh) will create and provision the virtual machine.
  * `vagrant up` will boot the VM (once it has been built).
  * `vagrant ssh` (from this directory) will create an ssh connection to the
      VM.
  * `vagrant halt` will stop the VM (i.e. shutdown properly the guest OS).

# Virtual network

The main directory of this repository contains the set of scripts to start a
virtual network as well as loads and apply its configuration files.
You _should_ only run such a network within the VM.

## Description
Each following scripts are executed in "[launch_network_group3.sh](launch_network_group3.sh)" (this script has to be executed as root with sudo):
For launch the network, we write differnt python scripts:
 * [router_config_creation.py](router_config_creation.py): This script write automatically every bird router configuration on the boot file, on the start file and on the bird file of every router. It allow to address each interface of every router.  
 * [host_config_creation.py](host_config_creation.py): This script create automatically every  Infrastructure and administration LAN.  
 * [service_config_creation.py](service_config_creation.py): This script create automatically every service LAN. Espacially, he create servers on each LAN (Monitoring, DNS, DHCP,...).

    -Don't forget to install the dhcp server : [sudo apt-get install isc-dhcp-server](sudo apt-get install isc-dhcp-server).

    -Don't forget to install the DNS server  : [sudo apt-get install bind9](sudo apt-get install bind9).
    
 * [firewall_config_creation.py](firewall_config_creation.py): This script write every firewall rules on each router by creating a bash script ([iptables/"router".sh](iptables/"router".sh)) for each router containing their rules firewall. In the end, I implement a script ([iptables/launchfirewall.sh](iptables/launchfirewall.sh)) he execute each script "[iptables/router.sh](iptables/router.sh)".
 After that, before creating the network, I launch by this command "[sudo sh iptables/launchfirewall.sh](sudo sh iptables/launchfirewall.sh)" my security on network.
 * "sudo [./cleanup.sh](./cleanup.sh)": For information a clean of network has been executed everytime in "[launch_network_group3.sh](launch_network_group3.sh)".

  - You can install nmap : [sudo apt-get install nmap](sudo apt-get install nmap).
 
 In pratice, for creating the entire network a Makefile has been written:
  * [make](make): command to execute -> "[./launch_network_group3.sh](./launch_network_group3.sh)".
  * make clean: can execute "sudo ./cleanup.sh" but it's not necessary because a clean of network are already realized before (see "For launch the network").
  * make connect namespace="name of router": execute sudo ./connect_to.sh group3_cfg $name of router. Connect on routers.
     "name of router": Hall, Pyth, Stev, Carn, Mich and SH1C.
  * make connect namespace="name of server": execute sudo ./connect_to.sh group3_cfg $name of server. Connect on servers.
     "name of server": Mon, DNS, DHCP, DNS2 and DHCP2.
     
# Tests
For part of routing you can go on [tests](tests/) directory where there are two subdirectories one for routing tests and an other for firewall tests.
For routing you can also find tests on Monitoring part (monitoring directory).

##Firewall
To test firewall: there are 3 scripts describe below:
    * [firewall_choose_port_test.sh](tests/firewall/firewall_choose_port_test.sh): launch the following commande "nmap -6 -p (port of chosen Protocol) (ip address of router interface or server interface)" the third parameter is the namespace where the nmap must be executed. 
    * [firewall_choose_test.sh](tests/firewall/firewall_choose_test.sh): launch another kind of nmap command with 2 parameters: the namespace where the command should be executed and the ip address of the interface.
    * [firewall_test.sh](tests/firewall/firewall_test.sh): this script check out different ports on Belneta and Belnetb.

To launch the scripts describe above:
    * make runTestFirewall_choose_port ns=? ip=? port=?: execute "```sudo sh tests/firewall/firewall_choose_port_test.sh ${ns} ${ip} ${port}```".
    * make runTestFirewall_choose_port ns=? ip=?: execute "```sudo sh tests/firewall/firewall_choose_port_test.sh ${ns} ${ip}```".
    * make runTestFirewall_firewall_border: execute  "```sudo sh tests/firewall/firewall_test.sh```".
    
  



