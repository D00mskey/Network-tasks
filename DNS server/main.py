from scapy.all import *

from Server import Server
from Cache import Cache
from config import *


if __name__ == '__main__':
    cache = Cache("cache.txt")
    cache.read_cache()
    try:
        server = Server(cache)
        sniff(filter=f'udp port {DNS_PORT}', prn=server.handle_dns_udp_packet)
    finally:
        cache.update()
