import json
import os
import stat


PATH='/home/vagrant/test/group3/lingi2142/'

db_local = open(PATH+"services/DNS/bind2/named_zones/zones/db.local","w")

db_local.write(
"$TTL	604800\n"
"@	IN	SOA	localhost. root.localhost. (\n"
"			      1		; Serial\n"
"			 604800		; Refresh\n"
"			  86400		; Retry\n"
"			2419200		; Expire\n"
"			 604800 )	; Negative Cache TTL\n"
";\n"
"@	IN	NS	localhost.\n"
"@	IN	A	127.0.0.1\n"
"@	IN	AAAA	::1\n"
	)
db_local.close()