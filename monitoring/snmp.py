import os
import time
from pysnmp.hlapi import *
from pysnmp.smi.view import MibViewController
from pyasn1.type.univ import *
import threading

TIME_INTERVAL = 10
TIME_WAIT_VALUE = 15
SNMP_PORT = 161 # Default port


def update_rrd(snmp_engine, user, upd_target, data):
    # Get data from agent
    get_data = getCmd(  snmp_engine,
                        user,
                        upd_target,
                        ContextData(),
                        *data)

    errorIndication, errorStatus, errorIndex, varBinds = next(get_data)
    if errorIndication:
        print(errorIndication)
        return 'error'
    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
        )
              )
        return 'error'
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


def ip_info(snmp_engine, user, upd_target):
    """Collects information about the IP packets going through this agent's interfaces"""
    data = (
        ObjectType(ObjectIdentity('IP-MIB', 'ipInReceives', 0)), # Total number of received input datagrams (including those received in error)
        ObjectType(ObjectIdentity('IP-MIB', 'ipInHdrErrors', 0)), # The number of input IP datagrams discarded due to errors in their IP headers.
        ObjectType(ObjectIdentity('IP-MIB', 'ipInAddrErrors', 0)), # The number of input IP datagrams discarded because the IP address in their IP header's destination field was not a valid address
        ObjectType(ObjectIdentity('IP-MIB', 'ipInUnknownProtos', 0)), # The number of locally-addressed IP datagrams received successfully but discarded because of an unknown or unsupported protocol
        ObjectType(ObjectIdentity('IP-MIB', 'ipForwDatagrams', 0)), # The number of input datagrams for which this entity was not their final IP destination and for which this entity attempted to find a route to forward them to that final destination
        ObjectType(ObjectIdentity('IP-MIB', 'ipInDiscards', 0)), # The number of input IP datagrams for which no problems were encountered to prevent their continued processing, but were discarded
        ObjectType(ObjectIdentity('IP-MIB', 'ipInDelivers', 0)), # The total number of datagrams successfully delivered to IP user-protocols
        ObjectType(ObjectIdentity('IP-MIB', 'ipOutRequests', 0)), # The total number of IP datagrams that local IP user-protocols  supplied to IP in requests for transmission
        ObjectType(ObjectIdentity('IP-MIB', 'ipOutNoRoutes', 0)), # The number of locally generated IP datagrams discarded because no route could be found to transmit them to their destination
        ObjectType(ObjectIdentity('IP-MIB', 'ipOutDiscards', 0)), # The number of output IP datagrams for which no problem was encountered to prevent their transmission to their destination, but were discarded
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0))
    )
    update_rrd(snmp_engine, user, upd_target, data)


class Agent_monitor(threading.Thread):
    def __init__(self, stop_event, agent, ip, snmpv3_user, data_collect_funs):
        threading.Thread.__init__(self)
        self.agent = agent
        self.stop_event = stop_event
        self.ip = ip
        self.snmpv3_user = snmpv3_user
        self.data_collect_funs = data_collect_funs

    def run(self):
        # Instantiate SNMP engine
        snmp_engine = SnmpEngine()

        # Specify which MIB to use
        mib_view_controller = snmp_engine.getUserContext('mibViewController')
        if not mib_view_controller:
            mib_view_controller = MibViewController(snmp_engine.getMibBuilder())

        # Instantiate user - SNMPv3
        user = UsmUserData(**self.snmpv3_user)

        # Instantiate transport protocol (UDP over IPv6)
        upd_target = Udp6TransportTarget((self.ip, SNMP_PORT)) 

        while not self.stop_event.is_set():
            for data_collect_fun in self.data_collect_funs:
                data_collect_fun(snmp_engine, user, upd_target)
            # Wait before getting next data
            stop_event.wait(TIME_INTERVAL)


"""MONITORING INITIALIZATION"""
# Infos
threads = []
stop_event = threading.Event()
snmpv3_user = {   
                'userName': 'gr1', 
                'authProtocol': usmHMACSHAAuthProtocol, # SHA (128bit)
                'authKey': 'password',
                'privKey': 'secret_key',
                'privProtocol': usmAesCfb128Protocol # AES (128bit)
            }

# Open conf file and initiate threads
with open('agent_list.conf', 'r') as f:
    for line in f:
        agent_name, agent_ip = line.split()
        print(agent_name,agent_ip)
        threads.append(Agent_monitor(stop_event, agent_name, agent_ip, snmpv3_user, [ip_info]))

# Start monitoring each agent
for th in threads:
    th.start()

# Stop monitoring
try:
    input('Type to terminate all threads')
except KeyboardInterrupt:
    stop_event.set()
    for th in threads:
        th.join()

# snmpget -v 3 -u gr1 -a SHA -x AES -A password -X secret_key -l authPriv 'udp6:fd00:300:3:f00::2' sysUpTime.0