#  DNS להדפיס את כל הדומיינים שעבורם מתבצעת שאילתת
from scapy.all import *

googolIP = ""

def print_query_name(dns_packet):
    """This function prints the domain name from a DNS query"""
    print(dns_packet[DNSQR].qname, "--", dns_packet[DNS]["DNS Resource Record"].rdata)

def filter_dns(packet):
    """This function filters query DNS"""
    # [DNS].opcode= Query  and [DNSQR].qtype = 1 - is type A
    if (DNS in packet and packet[DNS].opcode == 0 and packet[DNSQR].qtype == 1 and
                    packet.haslayer("DNS Resource Record")):
        # packet.show()
        global googolIP
        googolIP = packet[DNS]["DNS Resource Record"].rdata
        return True
    else:
        return False

print("Sending to google 'Hello'")
my_packet = IP(dst = "ynet.co.il")/ TCP(dport = 80) / Raw("Hello")
send(my_packet)

# print the DNS
sniff(lfilter=filter_dns, prn=print_query_name, timeout=10)

# -----------------------------------------------------------------
def getIP(domain):
    SERVER_IP = "8.8.8.8"
    DPORT = 53
    fullmsg = IP(dst=SERVER_IP)/UDP(dport=DPORT)/DNS(rd=1,qd=DNSQR(qname=domain))
    ans = sr1(fullmsg, verbose=0)
    # print(ans.show())
    print(domain + " -", ans["DNS"]["DNS Resource Record"].rdata)

getIP("google.co.il")
