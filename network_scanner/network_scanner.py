#!/usr/bin/env python

import scapy.all as scapy
import optparse


def get_ip_range():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="ip_range", help="Introduce IP range to scan")
    (options, arguments) = parser.parse_args()
    if options.ip_range is None:
        print("Please introduce an IP range to scan. For further info type --help")
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        clients_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(clients_dict)
    return clients_list


def print_result(results_list):
    if options.ip_range:
        print("IP\t\t\t\tMAC Address\n--------------------------------------------------")
        for client in results_list:
            print(client["ip"] + "\t\t\t" + client["mac"])
    else:
        exit()


options = get_ip_range()
scan_result = scan(options.ip_range)
print_result(scan_result)

