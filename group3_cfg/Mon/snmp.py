import time
import threading
import os
from pysnmp.hlapi import *
from pyasn1.type.univ import *

def get_info(agent, snmpEngine, user, udpTarget):

    # Data and get - http://cric.grenoble.cnrs.fr/Administrateurs/Outils/MIBS/?oid=1.3.6.1.2.1.4
    data = (
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)),
        ObjectType(ObjectIdentity('HOST-RESOURCES-MIB', 'hrSystemDate', 0)),
        ObjectType(ObjectIdentity('IP-MIB', 'ipInReceives', 0)),
        ObjectType(ObjectIdentity('IP-MIB', 'ipInHdrErrors', 0)),
        ObjectType(ObjectIdentity('IP-MIB', 'ipInAddrErrors', 0)),
        ObjectType(ObjectIdentity('IP-MIB', 'ipInUnknownProtos', 0)),
        ObjectType(ObjectIdentity('IP-MIB', 'ipInDiscards', 0)),
        ObjectType(ObjectIdentity('IP-MIB', 'ipInDelivers', 0)),
        ObjectType(ObjectIdentity('IP-MIB', 'ipOutRequests', 0)),
        ObjectType(ObjectIdentity('IP-MIB', 'ipOutDiscards', 0)),
        ObjectType(ObjectIdentity('IP-MIB', 'ipOutNoRoutes', 0))
    )

    get_data = getCmd(snmpEngine, user, udpTarget, ContextData(), *data)
    errorIndication, errorStatus, errorIndex, varBinds = next(get_data)

    # Directory
    directory = '/etc/log/snmp/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = directory + agent
    f = open(directory, "a")

    # Log
    if errorIndication:
        # print(errorIndication)
        return
    elif errorStatus:
        # print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        f.write('%s at %s\n' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for name, val in varBinds:
            # print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
            f.write('%s = %s\n' % (name.prettyPrint(), val.prettyPrint()))


class Monitor(threading.Thread):
    def __init__(self, agent, ip, user, function):
        threading.Thread.__init__(self)
        self.agent = agent
        self.ip = ip
        self.user = user
        self.function = function

    def run(self):
        snmpEngine = SnmpEngine()
        user = UsmUserData(**self.user)
        udpTarget = Udp6TransportTarget((self.ip, 161))

        while True:
            self.function[0](self.agent, snmpEngine, user, udpTarget)
            time.sleep(5)



# Variables
user = {
    'userName': 'myUser',
    'authProtocol': usmHMACSHAAuthProtocol,
    'authKey': 'sha1234sha',
    'privProtocol': usmAesCfb128Protocol,
    'privKey': 'aes1234aes'
}

agents = {
    'Hall-eth0':  'fd00:300:3:f06::1',
    'Hall-eth1':  'fd00:300:3:f00::1',
    'Pyth-eth0':  'fd00:300:3:f00::2',
    'Pyth-eth1':  'fd00:300:3:f02::2',
    'Pyth-eth2':  'fd00:300:3:f01::2',
    'Stev-eth0':  'fd00:300:3:f03::3',
    'Stev-eth1':  'fd00:300:3:f01::3',
    'Carn-eth0':  'fd00:300:3:f04::4',
    'Carn-eth1':  'fd00:300:3:f02::4',
    'Carn-eth2':  'fd00:300:3:f03::4',
    'Minch-eth0': 'fd00:300:3:f05::5',
    'Minch-eth1': 'fd00:300:3:f04::5',
    'SH1C-eth0':  'fd00:300:3:f05::6',
    'SH1C-eth1':  'fd00:300:3:f06::6'
}

# Start of the program
for ag_name, ag_ip in agents.items():
    Monitor(ag_name, ag_ip, user, [get_info]).start()


# snmpget -v 3 -u myUser -a SHA -x AES -A sha1234sha -X aes1234aes -l authPriv 'udp6:fd00:300:3:f00::2' sysUpTime.0