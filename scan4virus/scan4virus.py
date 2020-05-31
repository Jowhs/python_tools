#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyfiglet import Figlet
import subprocess
from tqdm import tqdm
from time import sleep

# spinner libraries
import itertools
import sys
import threading
import time

banner = Figlet(font='slant')
print(banner.renderText('SCAN4VIRUS'))

print("*****************************************************")
print("Requirements to use this tool:\n")
print("-Your operating system must be GNU/Linux\n")
print("-You need to have installed clamAV antivirus\n")
print("-You need to have installed python 3\n")
print("******************************************************")

FILE_PATH = "/home/testlite/virus-scan-report.txt"


class Spinner(object):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])

    def __init__(self):
        self.stop_running = threading.Event()
        self.spin_thread = threading.Thread(target=self.init_spin)

    def start(self):
        self.spin_thread.start()

    def stop(self):
        self.stop_running.set()
        self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            sys.stdout.write(next(self.spinner_cycle))
            sys.stdout.flush()
            time.sleep(0.25)
            sys.stdout.write('\b')


def update_virus_definitions():
    subprocess.call(["rm", "-Rf", "/var/log/clamav/freshclam.log"])
    print("Please wait, virus definitions are updating...\n")
    try:
        tasks = 100
        for i in tqdm(range(tasks), ascii=True):
            sleep(0.05)
        print("\n")

    except KeyboardInterrupt:
        print("Scanner canceled.")
    p = subprocess.Popen("freshclam", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    sleep(1)
    print("Virus definitions are now up to date.\n")
    print("---------------------------------------")
    sleep(2)


def give_permissions_to_file(file_path):
    return subprocess.call(["chmod", "755", file_path])


def quick_scan():
    print("Scanning...")
    spinner = Spinner()
    spinner.start()
    chmod = lambda file_path: subprocess.call(["chmod", "755", file_path])
    with open(FILE_PATH, "w") as f:
        subprocess.call(["clamscan", "-r", "-i", "/home/testlite/"], stdout=f)
        chmod(FILE_PATH)
    spinner.stop()

    fobj = open(FILE_PATH)
    found = fobj.read().strip().split()
    if "FOUND" in found:
        print("\n VIRUS DETECTED. PLEASE CHECK FILE ON " + FILE_PATH + " FOR MORE INFO.")
    else:
        print('\n Scan completed successfully. NOT VIRUS FOUND')
    fobj.close()

    result = open(FILE_PATH, "r")
    print(result.read())


def deep_scan():
    print("Scanning...")
    spinner = Spinner()
    spinner.start()
    with open(FILE_PATH, "w") as f:
        subprocess.call(["clamscan", "-r", "-i", "/"], stdout=f)
        give_permissions_to_file(FILE_PATH)
    spinner.stop()

    fobj = open(FILE_PATH)
    found = fobj.read().strip().split()
    if "FOUND" in found:
        print("\n VIRUS DETECTED. PLEASE CHECK FILE ON " + FILE_PATH + "FOR MORE INFO.")
    else:
        print('\n Scan completed successfully. NOT VIRUS FOUND')
    fobj.close()


update_virus_definitions()

print("What type of scan do you want to run?: \n")
print("1-Quick scan.\n")
print("2-Deep scan (Can take several minutes or even hours).\n")

while True:
    try:
        option = int(input("Choose an option: "))

        if option == 1:
            quick_scan()
            break
        elif option == 2:
            deep_scan()
            break
        else:
            print("Please choose 1 or 2")

    except ValueError:
        print("Please select a number: 1 or 2")
