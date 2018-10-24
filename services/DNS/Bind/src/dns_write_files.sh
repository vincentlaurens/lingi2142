#!/usr/bin/env python3
import json
import os
import stat
#import sys

#dns = sys.argv[1]
PATH = "/home/vagrant/lingi2142/network_server"
#File namedX.conf
dns_conf = open(PATH+"/bind/named_zones/named.conf", "w")

dns_conf.write(
"include \"/etc/bind/named.conf.options\";\n"
"include \"/etc/bind/named.conf.local\";\n"
"include \"/etc/bind/named.conf.log\";\n"
)

dns_conf.close()

dns_conf_local = open(PATH+"/bind/named_zones/named.conf.local", "w")




dns_conf_local.write(
"//\n"
"// Do any local configuration here\n"
"//\n"
"\n"
"//Zone group3.ingi : public zone\n"
"zone \"group3.ingi\" IN {\n"
"    type master;\n"
"    file \"/etc/bind/zones/db.group3.ingi\";\n"
"};\n"
"\n"

"\n"
"//Zone 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.3.0.0.0.0.0.2.0.0.0.d.f.ip6.arpa : public zone\n"
"zone \"1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.3.0.0.0.0.0.2.0.0.0.d.f.ip6.arpa\" IN {\n"
"    type master;\n"
"    file \"/etc/bind/zones/db.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.3.0.0.0.0.0.2.0.0.0.d.f.ip6.arpa\";\n"
"};\n"
"\n"

	)

dns_conf_local.close()




dns_conf_options = open(PATH+"/bind/named_zones/named.conf.options", "w")



dns_conf_options.write(


	)

dns_conf_options.close()