#!/usr/bin/env python3
import json
import os
import stat

#from ../../../constants import PATH
PATH='/home/vagrant/test/group3/lingi2142/services/DNS'

dns_conf = open(PATH+"services/DNS/bind/named_zones/named.conf", "w")
dns_conf.write(
"include \"/etc/bind/named.conf.options\";\n"
"include \"/etc/bind/named.conf.local\";\n"
"include \"/etc/bind/named.conf.log\";\n"
)

dns_conf.close()

dns_conf_local = open(PATH+"services/DNS/bind/named_zones/named.conf.local", "w")




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
"//Zone 3.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.3.0.0.0.0.0.2.0.0.0.d.f.ip6.arpa : public zone\n"
"zone \"3.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.3.0.0.0.0.0.2.0.0.0.d.f.ip6.arpa\" IN {\n"
"    type master;\n"
"    file \"/etc/bind/zones/db.3.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.3.0.0.0.0.0.2.0.0.0.d.f.ip6.arpa\";\n"
"};\n"
"\n"

	)

dns_conf_local.close()




dns_conf_options = open(PATH+"services/DNS/bind/named_zones/named.conf.options", "w")



dns_conf_options.write(
"//\n"
"acl intern_user {\n"
	"fd00:200:3::/48;\n"
	"fd00:300:3::/48;\n"
"};\n"
"\n"
"\n"
"options {\n"
       "directory \"/var/cache/bind/ns1\";\n"
       "pid-file  \"/var/run/named_ns1.pid:\";\n"
       "forward first;\n"
       "forwarders { fd00::d; };\n"
       "auth-nxdomain no;\n"
	"listen-on-v6 { any; };\n"
       "allow-transfer { fd00::; };\n"
       "allow-query { any; };\n"
       "allow-recursion { intern_user; }\n;"
       "allow-query-cache { intern_user;};\n"
       "version none;\n"
"};\n"

	)

dns_conf_options.close()


dns_conf_log = open(PATH+"services/DNS/bind/out/named.conf.log", "w")

dns_conf_log.write(
"logging {\n"
"  channel bind_log {\n"
"    file \"/var/log/bind/bind.log\" versions 3 size 5m;\n"
"    severity info;\n"
"    print-category yes;\n"
"    print-severity yes;\n"
"    print-time yes;\n"
"  };\n"
"        category default { bind_log; };\n"
"        category lame-servers { null; };\n"
"        category update { bind_log; };\n"
"        category update-security { bind_log; };\n"
"        category security { security_info; };\n"
"};\n"

)
dns_conf_log.close()

