#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import subprocess
# import optparse
# import re
# import time
import random
from pyfiglet import Figlet

banner = Figlet(font='slant')
print(banner.renderText('MAC CHANGER'))


def spoof_mac():
    while True:
        try:
            print("1-Lenovo")
            print("2-Hewlett Packard")
            print("3-Dell")
            print("4-Apple")
            print("5-Acer")
            print("6-Asus")
            print("7-Toshiba")
            print("8-Samsung")
            print("9-LG")
            oui_mac = str()
            laptops = int(input("Choose a vendor from the list: \n"))
            if laptops == 1:
                oui_mac = "14:36:c6:"
            elif laptops == 2:
                oui_mac = "68:b5:99:"
            elif laptops == 3:
                oui_mac = "b8:2a:72:"
            elif laptops == 4:
                oui_mac = "bc:4c:c4:"
            elif laptops == 5:
                oui_mac = "c0:98:79:"
            elif laptops == 6:
                oui_mac = "e0:3f:49:"
            elif laptops == 7:
                oui_mac = "00:1c:7e:"
            elif laptops == 8:
                oui_mac = "00:1f:cc:"
            elif laptops == 9:
                oui_mac = "00:26:e2:"
        except ValueError:
            print("Please select a number from the list")
            continue
        else:
            break

    alphanumeric = ["a", "b", "c", "d", "e", "f", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    rand_mac = f'{random.choice(alphanumeric)}{random.choice(alphanumeric)}:' \
               f'{random.choice(alphanumeric)}{random.choice(alphanumeric)}:' \
               f'{random.choice(alphanumeric)}{random.choice(alphanumeric)}'

    new_mac = oui_mac + rand_mac
    print(new_mac)


spoof_mac()

#
#
# def change_mac(interface, mac_addr):
#     original_mac = subprocess.check_output(["ifconfig"])
#     original_mac_res = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", original_mac)
#
#     subprocess.call(["ifconfig", interface, "down"])
#     subprocess.call(["ifconfig", interface, "hw", "ether", mac_addr])
#     subprocess.call(["ifconfig", interface, "up"])
#
#     print("[+] Changing mac address for interface " + interface + " to " + mac_addr + "\n")
#     print("Executing ifconfig command ...")
#     time.sleep(5)
#     print(subprocess.check_output(["ifconfig eth0", options.interface]))
#
#     print("Verifying changes ...")
#     time.sleep(5)
#     spoof_mac = subprocess.check_output(["ifconfig eth0"])
#     spoof_mac_res = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", spoof_mac)
#     print("Successfully MAC address change from " + original_mac_res.group(0) + " to: " + spoof_mac_res.group(0))
#
#
# change_mac(eth0, spoofed_mac)
