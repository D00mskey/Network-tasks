import socket
from config import DNS_PORT, DESTINATION

requests = {
    'vk': b"\x75\xa3\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x02\x70\x75\x02"
          b"\x76\x6b\x03\x63\x6f\x6d\x00\x00\x01\x00\x01"}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)
sock.sendto(requests['vk'], (DESTINATION, DNS_PORT))
print('Request was sent')
