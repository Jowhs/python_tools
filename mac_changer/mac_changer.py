#!/usr/bin/env python

import subprocess
import optparse
import re
import time


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if options.interface is None:
        parser.error("[-] Is mandatory introduce an interface, for more info --help")
    elif options.new_mac is None:
        parser.error("[-] Is mandatory introduce a mac address, for more info --help")
    return options


def change_mac(interface, mac_addr):
    original_mac = subprocess.check_output(["ifconfig"])
    original_mac_res = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", original_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_addr])
    subprocess.call(["ifconfig", interface, "up"])

    print("[+] Changing mac address for interface " + interface + " to " + mac_addr + "\n")
    print("Executing ifconfig command ...")
    time.sleep(5)
    print(subprocess.check_output(["ifconfig", options.interface]))

    print("Verifying changes ...")
    time.sleep(5)
    spoof_mac = subprocess.check_output(["ifconfig", options.interface])
    spoof_mac_res = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", spoof_mac)
    print("Successfully MAC address change from " + original_mac_res.group(0) + " to: " + spoof_mac_res.group(0))


options = get_arguments()
change_mac(options.interface, options.new_mac)
