#!/usr/bin/env python3
import json
import os
import stat


PATH='/home/vagrant/test/group3/lingi2142/'

db_group3 = open(PATH+"services/DNS/bind/named_zones/zones/db.group3.ingi","w")

db_group3.write(
"$TTL 10800\n"
"@   IN SOA  @ group3.ingi. admin.group3.ingi.(\n"
"            2   	 ; serial\n"
"            7200    ; refresh \n"
"            900     ; retry   \n"
"            1209600 ; expire  \n"
"            3600 )  ; minimum \n"


"@               IN        NS        ns1.group3.ingi. \n"
"@               IN        NS        ns2.group3.ingi. \n"
"@               IN        TXT       \"zone group3\" \n"
"ns1             IN        AAAA      fd00:300:3:f061::53 \n"
"ns2             IN        AAAA      fd00:300:3:f012::53 \n"

"carn             IN        AAAA      fd00:300:3:f04::4 \n"
"carn             IN        AAAA      fd00:300:3:f03::4 \n"
"carn             IN        AAAA      fd00:300:3:f02::4 \n"

"hall             IN        AAAA      fd00:300:3:f06::1 \n"
"hall             IN        AAAA      fd00:300:3:f00::1 \n"

"mich             IN        AAAA      fd00:300:3:f05::5 \n"
"mich             IN        AAAA      fd00:300:3:f04::5 \n"

"pyth             IN        AAAA      fd00:300:3:f00::2 \n"
"pyth             IN        AAAA      fd00:300:3:f02::2 \n"
"pyth             IN        AAAA      fd00:300:3:f01::2 \n"

"sh1c             IN        AAAA      fd00:300:3:f05::6 \n"
"sh1c             IN        AAAA      fd00:300:3:f06::6 \n"

"stev             IN        AAAA      fd00:300:3:f03::3 \n"
"stev             IN        AAAA      fd00:300:3:f01::3 \n"
)
db_group3.close()

db_group3_reverse = open(PATH+"services/DNS/bind/named_zones/zones/db.reverse.group3.ingi","w")

db_group3_reverse.write(
	"	$TTL 1h	; Default TTL\n"
	"@	IN	SOA	ns1.group3.ingi. (\n"
	"	2018102401	; serial\n"
	"	2h		;\n"
	"	15m		;\n"
	"	2w		;\n"
	"	1h		;\n\n\n"

	"@	IN	NS	ns1.group3.ingi\n"
	"@	IN	NS	ns2.group3.ingi\n"
	"; IPv6 PTR entries\n"
	"3.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.6.0.f.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    ns1.group3.ingi.\n"
	"3.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2.1.0.f.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    ns2.group3.ingi.\n"
	"4.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.4.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    carn.group3.ingi.\n"
	"4.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.3.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    carn.group3.ingi.\n"
	"4.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    carn.group3.ingi.\n"
	"1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.6.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    hall.group3.ingi.\n"
	"1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    hall.group3.ingi.\n"
	"5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.5.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    mich.group3.ingi.\n"
	"5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.4.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    mich.group3.ingi.\n"
	"2.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    pyth.group3.ingi.\n"
	"2.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    pyth.group3.ingi.\n"
	"2.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    pyth.group3.ingi.\n"
	"6.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.5.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    sh1c.group3.ingi.\n"
	"6.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.6.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    sh1c.group3.ingi.\n"
	"3.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.3.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    stev.group3.ingi.\n"
	"3.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.f.0.3.0.0.0.0.0.3.0.0.0.d.f.ip6.arpa.    IN    PTR    stev.group3.ingi.\n"

	)


db_group3.close()