#!/usr/bin/env python

import requests


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "anyweb.com"
with open("/root/python/hack_tools/crawler/fildir.txt") as wordlist:
    for line in wordlist:
        test_url = target_url + "/" + line.strip()
        response = request(test_url)
        if response:
            print("[+] Directory or file exists: " + test_url)
