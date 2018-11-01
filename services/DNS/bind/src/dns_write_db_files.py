#!/usr/bin/env python3
import json
import os
import stat


from ../../../constants import PATH

PATH = PATH+"services/DNS"

db_group3 = open(PATH+"/bind/out/zones/db.group3.ingi","w")

db_group3.write(
"$TTL 10800\n"
"@   IN SOA  @ group3.ingi.(\n"
"            2   	 ; serial\n"
"            7200    ; refresh \n"
"            900     ; retry   \n"
"            1209600 ; expire  \n"
"            3600 )  ; minimum \n"
)

db_group3.write("@             IN        NS        ns1.group3.ingi. \n")
db_group3.write("@             IN        TXT       \"zone group3\" \n")
db_group3.write("@             IN        AAAA      fd00:200:3:1000::53 \n")
db_group3.write("@             IN        AAAA      fd00:300:3:1000::53 \n")

db_group3.close()

db_group3_reverse = open(PATH+"/bind/out/zones/db.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.3.0.0.0.0.0.2.0.0.0.d.f.ip6.arpa","w")

db_group3_reverse.write(
"	$TTL 1h	; Default TTL\n"
"@	IN	SOA	ns1.group3.ingi. (\n"
"	2018102401	; serial\n"
"	2h		;\n"
"	15m		;\n"
"	2w		;\n"
"	1h		;\n"
	)
db_group3_reverse.write("@	IN	NS	ns1.group3.ingi")
db_group3_reverse.write("3.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.3.0.0.0.0.0.2.0.0.0.d.f.ip6.arpa.    IN    PTR    ns1.group3.ingi.")


db_group3.close()