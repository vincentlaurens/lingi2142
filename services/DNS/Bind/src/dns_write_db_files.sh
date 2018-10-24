#!/usr/bin/env python3
import sys
import json
import os

sys.path.append('/home/vagrant/lingi2142/')
from constants import PREFIXES, PATH

PATH = PATH+"end_user_management"

###########################################
# Configuration db.group3.ingi            #
###########################################
db_group3 = open(PATH+"/bind/out/zones/db.group3.ingi","w")

db_group3.write(
"$TTL 10800\n"
"@   IN SOA  @ group3.ingi.(\n"
"            2   	 ; serial\n"
"            7200    ; refresh  (  2   hours)\n"
"            900     ; retry    (  15  min)\n"
"            1209600 ; expire   (  2   weeks)\n"
"            1800 )  ; minimum  (  30  min)\n"
)

db_group3.write("@             IN        NS        ns1.group3.ingi. \n")
db_group3.write("@             IN        TXT       \"zone group3\" \n")
db_group3.write("@             IN        AAAA      fd00:200:3:1000::1 \n")
db_group3.write("@             IN        AAAA      fd00:300:3:1000::1 \n")

db_group3.close()

db_group3_reverse = open(PATH+"/bind/out/zones/db.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.3.0.0.0.0.0.2.0.0.0.d.f.ip6.arpa","w")

db_group3_reverse.write(
"	$TTL 1h	; Default TTL\n"
"@	IN	SOA	ns1.group3.ingi. (\n"
"	2018102401	; serial\n"
"	1h		; slave refresh interval\n"
"	15m		; slave retry interval\n"
"	1w		; slave copy expire time\n"
"	1h		; NXDOMAIN cache time\n"
	)
db_group3_reverse.write("@	IN	NS	ns1.group3.ingi")
db_group3_reverse.write("1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.3.0.0.0.0.0.2.0.0.0.d.f.ip6.arpa.    IN    PTR    ns1.group3.ingi.")


db_group3.close()