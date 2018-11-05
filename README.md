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
Each following scripts are executed in "[launch_network_group3.sh](launch_network_group3.sh)":
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
  * [make](make): command to execute -> "./launch_network_group3.sh".
  * make clean: can execute "[sudo ./cleanup.sh](sudo ./cleanup.sh)" but it's not necessary because a clean of network are already realized before (see "For launch the network").
  * make "name of router": execute sudo [./connect_to.sh group3_cfg $name of router](./connect_to.sh group3_cfg $name of router). Connect on routers.
     "name of router": Hall, Pyth, Stev, Carn, Mich and SH1C.
  * make "name of server": execute sudo [./connect_to.sh group3_cfg $name of server](./connect_to.sh group3_cfg $name of server). Connect on servers.
     "name of server": Mon, DNS, DHCP, DNS2 and DHCP2.
  



