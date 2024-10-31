import scapy

from scapy.all import sniff, IP, ICMP

def icmp_packet_handler(packet):
    if IP in packet and ICMP in packet and packet[IP].ttl == 1:
        packet.show()

def receive_icmp_packet():
    sniff(filter="icmp", prn=icmp_packet_handler)

if __name__ == "__main__":
    receive_icmp_packet()
