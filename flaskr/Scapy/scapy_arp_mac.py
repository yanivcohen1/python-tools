#  DNS להדפיס את כל הדומיינים שעבורם מתבצעת שאילתת
from scapy.all import *

# cap = sniff(count=15)
def is_good(packet):
    if (packet.haslayer(ARP)):
      # packet.show()
      print("mac:", packet[ARP].hwsrc, "- ip:", packet[ARP].psrc)
      return True
    else:
      return False

# print the mac number
cap = sniff(lfilter=is_good, timeout=15)
