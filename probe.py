#!/usr/bin/env python
import subprocess
import socket
import struct
import sys
from telnetlib import Telnet

DEFAULT_USER = 'admin'
DEFAULT_PASSWORD = 'admin'
PORT = 4719
IP_START = '127.0.0.1'
IP_END = '127.0.0.254'

DEFAULT_TIMEOUT = 3

def _do_probe(ip_address, port, user, password):
    try:
        client = Telnet(ip_address, port, DEFAULT_TIMEOUT)
        client.read_until('login: ')
        client.write(user + '\n')
        client.read_until('Password: ')
        client.write(password + '\n')
        client.write('exit\n')
        client.close()
        return True
    except:
        return False

def probe(ip_start, ip_end, port, user, password, num_processes=1):
    current_ip = struct.unpack('!L', socket.inet_aton(ip_start))[0]
    ip_end = struct.unpack('!L', socket.inet_aton(ip_end))[0]
    total_ips = ip_end - current_ip
    if total_ips < 0:
        total_ips = -total_ips
        # swap the range endpoints
        current_ip, ip_end = ip_end, current_ip
    total_ips += 1
    print 'Starting to test %d IP address%s.' % (
        total_ips,
        'es' if total_ips > 1 else ''
    )
    current_dec = 0
    probed_ips = 0
    total_weaklings = 0

    while current_ip <= ip_end:
        probing_ip = struct.pack('!L', current_ip)
        if _do_probe(probing_ip, port, user, password):
            total_weaklings += 1
            print 'Weakling: ' + probing_ip
        current_ip += 1
        probed_ips += 1
        scanned = probed_ips * 1.0 / total_ips
        if scanned * 10 > current_dec:
            current_dec += 1
            print 'Scanned %d%% of the IP range' % (scanned * 100)
    print 'Found %d weaklings' % total_weaklings

if __name__ == '__main__':
    if len(sys.argv) == 1:
        ip_start = IP_START
        ip_end = IP_END
        user = DEFAULT_USER
        password = DEFAULT_PASSWORD
    elif len(sys.argv) == 3:
        ip_start = sys.argv[1]
        ip_end = sys.argv[2]
        user = DEFAULT_USER
        password = DEFAULT_PASSWORD
    elif len(sys.argv) == 5:
        ip_start = sys.argv[1]
        ip_end = sys.argv[2]
        user = sys.argv[3]
        password = sys.argv[4]
    probe(ip_start, ip_end, PORT, user, password)

