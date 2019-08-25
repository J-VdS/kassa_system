#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from escpos import printer
import socket #communicatie met de kassa
import queue  #bestellingen
import pickle #
#from threading import Thread

#network constants
ip = "0.0.0.0"
poort = 1741

#Printer contants
#https://github.com/python-escpos/python-escpos/issues/230
ID_VENDOR = 0x0456  #hex 0xabcd
ID_PRODUCT = 0x808 #hex 0xabcd
OUT_END = 0x81 #hex
IN_END = 0x03 #hex

printer_obj = None
print_queue = queue.Queue()

#STOP LOOP
STOP_LOOP = False


def start_listening():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, poort))
    
    s.listen()
    #In principe is er maar 1 connectie en dat is met de kassa!
    
    s.close()


def open_printer():
    global printer_obj
    printer_obj = printer.Usb(ID_VENDOR, ID_PRODUCT, 0, IN_END, OUT_END)
    

def close_printer():
    global printer_obj
    printer_obj.close()


def start_printloop():
    #loopt in thread
    open_printer()
    try:
        while not(STOP_LOOP):
            if not(print_queue.empty()):
                print_command = print_queue.get()
                #verwerk(print_command)
                #verwerk de data en stuur naar de printer
    except Exception as e:
        print(e)
        #schrijf ook alle error naar een file want programma loopt wss in een lus
    
    finally:
        close_printer()
     

if __name__ == "__main__":
    pass
    


