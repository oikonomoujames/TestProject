import scapy
from scapy.all import *
from ospf import *
"""
p = IP()/OSPF_Hdr()/OSPF_LSReq(requests=[OSPF_LSReq_Item()])
p.show2()
send(p)
"""
"""
# TTL needs to be 1 for local networks as per RFC 3171
packet = IP(src='10.0.0.1', dst='224.0.0.5', ttl=1)
packet = packet/OSPF_Hdr(version='2', type="Hello", src='10.0.0.1', area='0.0.0.1')
# packet = packet/OSPF_Hdr(version='2', type='1', src='10.0.0.1', area='0.0.0.1')
packet.show()
#packet = packet/OSPF_Hello()
packet = packet/OSPF_Hello(router='172.17.2.2', backup='172.17.2.1', neighbor='172.17.2.1')
packet.show()
"""

packet = IP(src='172.17.2.2', dst='224.0.0.5', ttl=1)
# OSPF Header:
#   Version (8bit): 2|3
#   Type (8bit): 1 Hello|2 DB Descriptor|3 Link state Request|4 Link state Update|5 Link state Ack
#   Packet Length (16bit)
#   Router ID (32 bit)
#   Area ID (32 Bit)
#   Checksum (16 bit)
#   Authentication type (16 Bit)
#   Authentication Data (32 bit)
packet = packet/OSPF_Hdr(version=2,
                         type="Hello",
                         src='172.17.2.2',
                         area='0.0.0.1')
# OSPF Hello Packet:
#   mask (32bit)
#   Hello interval (16bit): Integer in secs
#   Options (8bit): (Set an decimal integer. That number will correspond to the binary number for the options)
#       DN: (options=128)
#       O: (options=64)
#       DC (Demand Circuits): (options=32)
#       L (LLS Data block): (options=16)
#       N (NSSA): (options=8)
#       MC (Multicast): (options=4)
#       E (External routing): (options=2)
#       MT (Multi-topology routing): (options=1)
#   Priority (8 bit): This is the BR/BDR priority
#   Dead interval (32 Bit): Integer in secs
#   Designated router (32 bit): The router ID of the DR. If the network does not support a DR this field is 0.0.0.0
#   Backup Designated router (32 bit): The router ID of the BDR.
#                                      If the network does not support a DR this field is 0.0.0.0
#   Neighbors (32 Bit): All the devices that have sent a hello packet on the connecting link will be listed here.
#                       Variable length field
packet = packet/OSPF_Hello(mask='255.255.255.255',
                           hellointerval=11,
                           options=0,
                           prio=1,
                           deadinterval=5,
                           router='172.17.2.2',
                           backup='172.17.2.1',
                           neighbors=['172.17.2.1', '172.17.2.2'])
packet.show()
send(packet)
