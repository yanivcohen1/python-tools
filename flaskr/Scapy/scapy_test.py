#  DNS להדפיס את כל הדומיינים שעבורם מתבצעת שאילתת
from scapy.all import *

def print_query_name(dns_packet):
    """This function prints the domain name from a DNS query"""
    print(dns_packet[DNSQR].qname)

def filter_dns(packet):
    """This function filters query DNS"""
    return (DNS in packet and packet[DNS].opcode == 0 and packet[DNSQR].qtype == 1)

print("Sending to google 'Hello'")
my_packet = IP(dst = "www.google.com") / Raw("Hello")
send(my_packet)

print("Starting to sniff!")
sniff(count=10, lfilter=filter_dns, prn=print_query_name)

# -----------------------------------------------------------------

def is_good(packet):
    return (TCP in packet and (packet[TCP].sport == 80 or packet[TCP].dport == 80))

def print_packet(packet):
    print(packet[IP].src, "-", packet[IP].dst)

sniff(count=3, lfilter=is_good, prn=print_packet)