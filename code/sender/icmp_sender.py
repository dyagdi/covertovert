import scapy

# Implement your ICMP sender here
from scapy.all import IP, ICMP, send

def send_icmp_packet():
    packet = IP(dst="receiver", ttl=1) / ICMP()
    send(packet)

if __name__ == "__main__":
    send_icmp_packet()
