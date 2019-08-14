#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial #communicatie met de printer via usb
import socket #communicatie met de kassa
import queue  #bestellingen
import pickle #
from threading import Thread

ip = "0.0.0.0"
poort = 1741


def start_listening():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, poort))
    
    s.listen()
    #In principe is er maar 1 connectie en dat is met de kassa!
    
    s.close()
    
if __name__ == "__main__":
    pass