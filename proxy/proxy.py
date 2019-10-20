#!/usr/bin/env python

import netfilterqueue


def process_packet(packet):
    print(packet)
    packet.accept() # Forward the connection
    # packet.drop() -> Cut the connection


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
