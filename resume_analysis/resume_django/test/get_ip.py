import os

import socket, fcntl, struct

def get_ip2(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

if __name__ == '__main__':
    print (get_ip2('eth0'))
    print (get_ip2('lo'))