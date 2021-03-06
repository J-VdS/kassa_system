#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#TODO; stuur bevestiging aangekomen en geprint
#TODO: sluit connectie met de printer indien de queue leeg is, heropen indien er terug een bestelling is

import time

import socket #communicatie met de kassa
import queue  #bestellingen
import pickle #decode data
import select #socket verkeer
#from escpos import *
from threading import Thread, Condition

#error handling
import sys 

try:
    from escpos.printer import Usb
    LIB = True
except:
    print("escpos module isn't installed on this system\n We will print everything in the console instead.\nThe prefix is [EP]")
    LIB = False    

#network constants
IP = "0.0.0.0"
POORT = 1741
HEADERLENGTH = 10
NAAM = "printer" #TODO extra veld moet doorgestuurd worden en na de eerste verbinding wordt de naam vastgelegd
TBT = 5 #tijd tussen 2 tickets (in seconden)
#debug
DYNCON = True #dynamische seriële connectie
LOGGING = True
ALLLOGGING = True
if LOGGING:
    import os, traceback
    if not(os.path.isdir("logs")):
        os.mkdir("logs")
    FILENAME = os.path.join("logs", "errlog{}.log".format(int(time.time()))) #https://www.unixtimestamp.com/index.php
else:
    FILENAME = None
    
if ALLLOGGING:
    import os
    if not(os.path.isdir("logs")):
        os.mkdir("logs")
    sys.stderr = open(os.path.join("logs", "log{}.log".format(int(time.time()))), 'w')
    sys.stdout = sys.stderr
#Printer contants
#https://github.com/python-escpos/python-escpos/issues/230
#breedte is 32 wss

#epson printer

ID_VENDOR = 0x04b8 #hex 0xabcd
ID_PRODUCT = 0x0202 #hex 0xabcd
OUT_END = 0x01  #hex
IN_END = 0x82 #hex
'''
#hoin printer
ID_VENDOR = 0x0456  #hex 0xabcd
ID_PRODUCT = 0x0808 #hex 0xabcd
OUT_END = 0x03 #hex
IN_END = 0x81 #hex
'''
#printer_obj = None
print_queue = queue.Queue()  # bevat alle bestellingen die moeten worden afgedrukt
print_status = queue.Queue() # bevat alle statusberichten over de bestellingen (succes/gefaald/bezig)

#STOP LOOP
STOP_LOOP = False


#verwerkt de data
def handles_message(client_socket):
    try:
        message_header = client_socket.recv(HEADERLENGTH)
        
        #connection closed
        if not len(message_header):
            return 0
        
        lengte = int(message_header.decode("utf-8"))
        #print("lengte:", lengte)
        data = client_socket.recv(lengte) #pickled-data
        #print("unpickled:", pickle.loads(data))
        return pickle.loads(data) #dict bevat request en eventuele data
    except:
        return 0


#vorm data om
def makeMsg(msg):
    '''
        <dict> msg
    '''
    msg = pickle.dumps(msg)
    msg_header = f"{len(msg):<{HEADERLENGTH}}".encode('utf-8')  
    return msg_header + msg


def start_listening():
    global STOP_LOOP
    global print_queue
    cond = Condition()
    Thread(target=start_printloop, args=(cond,), daemon=False).start() #geen deamon!
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((IP,POORT))
    
    s.listen()
    #In principe is er maar 1 connectie en dat is met de kassa!
    
    #lijst met sockets
    sockets_list = [s]
    addr_info_sock = []
    addr_info_ip = []
    
    try:
        print("Aan het luisteren voor connecties op: {0}:{1}".format(IP, POORT))
        while not(STOP_LOOP):
            # Calls Unix select() system call or Windows select() WinSock call with three parameters:
            #   - rlist - sockets to be monitored for incoming data
            #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
            #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
            # Returns lists:
            #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
            #   - writing - sockets ready for data to be send thru them
            #   - errors  - sockets with some exceptions
            # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
            
            # Iterate over notified sockets
            for notified_socket in read_sockets:
        
                # If notified socket is a server socket - new connection, accept it
                if notified_socket == s:
        
                    # Accept new connection
                    # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                    # The other returned object is ip/port set
                    print("accept")
                    client_socket, client_address = s.accept()
                    print(client_address)
                    addr_info_sock.append(client_socket)
                    addr_info_ip.append(client_address)
                    #terug toevoegen want zal direct een bericht sturen
                    read_sockets.append(client_socket)
        
                    '''#ontvang
                    lengte = int(client_socket.recv(HEADERLENGTH).decode("utf-8"))
                    print("lengte:",lengte)
                    if not lengte:
                        client_socket.close()
                        continue
                    data = pickle.loads(client_socket.recv(lengte))
                    print(data)
                    
                    # Add accepted socket to select.select() list
                    sockets_list.append(client_socket)
                            
                    # Also save username and username header
                    connecties[client_socket] = data['naam']
                    
                    #print mss ook de naam
                    print('Accepted new connection from {}:{}'.format(client_address, data['naam']))
                    '''
                # Else existing socket is sending a message
                else:                    
                    # Receive message
                    print("bericht")
                    message = handles_message(notified_socket)
                    
                    # Get user by notified socket, so we will know who sent the message
                    #user = connecties[notified_socket]
                    
                    # If False, client disconnected, cleanup
                    if not(message):
                        #print(f"Connectie met {user} gesloten!")
                        #gebruik conn.close() om de connectie te sluiten!
                        # Remove from list for socket.socket()
                        sockets_list.remove(notified_socket)
                        
                        if notified_socket in addr_info_sock:
                            index = addr_info_ip.index(notified_socket)
                            del addr_info_sock[index]
                            del addr_info_ip[index]
        
                        # Remove from our list of users
                        #del connecties[notified_socket]
                        notified_socket.close() #mss ni nodig - close connection
                        
                        continue
                    
                    message["addr"] = addr_info_ip[addr_info_sock.index(notified_socket)]
                    
                    with cond:
                            print_queue.put(message)
                            cond.notify()

                    if "STOP" in message:
                        STOP_LOOP = True
                        break


            # It's not really necessary to have this, but will handle some socket exceptions just in case
            for notified_socket in exception_sockets:
                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)
    
    
    except Exception as e:
        print("Error ", e)
        STOP_LOOP = True
    finally:
        for sock in sockets_list:
            if sockets_list != s:
                sock.close()
        s.close()


def open_printer():
    try:
        if LIB:
            p = Usb(ID_VENDOR,ID_PRODUCT,0,IN_END,OUT_END)
        else:
            p = fakePrinter(ID_VENDOR,ID_PRODUCT,0,IN_END,OUT_END)
    except Exception as e:
        print("[EP]", e, "using a fake printer instead")
        p = fakePrinter(ID_VENDOR,ID_PRODUCT,0,IN_END,OUT_END)
    return p
    

def close_printer(printer):
    printer.close()
    
    
def start_printloop(conditie):
    global STOP_LOOP
    global print_queue
    
    print("start loop")
    
    if DYNCON:
        printer = None
    else:
        printer = open_printer()
    
    try:
        #hij zal enkel afsluiten indien de print_queue leeg is en de connectie gesloten is!
        while not(STOP_LOOP) or not(print_queue.empty()):
            #close connection with the printer if there is no queue
            if print_queue.empty() and DYNCON and not(printer is None):
                close_printer(printer)
                printer = None

            with conditie:
                while print_queue.empty():
                    print(" --- wait --- ")
                    conditie.wait()
            #reopen connectie met printer
            if DYNCON and printer is None:
                printer = open_printer()
                if isinstance(printer, fakePrinter):
                    print_status.put(("alg", "FAKE", -2))
            #stuur naar de printer
            ret = printer_verwerk(printer, print_queue.get())
            if not(ret):
                break
            time.sleep(TBT)
    except Exception as e:
        print(e)
        #schrijf ook alle error naar een file want programma loopt wss in een lus
    finally:
        #als dit mogelijk is
        close_printer(printer)
         
        
def printer_verwerk(printer_obj, obj):
    if "STOP" in obj:
        return False
    '''	    
    try:
        #check of printer nog papier heeft
        #https://github.com/python-escpos/python-escpos/issues/143
        printer_obj.device.write(OUT_END, "\x10\x04\x04", 5000) 
        #weet niet of dit werkt
        ret = printer_obj.device.read(IN_END, 256, 5000)
    except Exception as e:
        print("Papiererror: ", e)
    '''
    try:
        #print en verwerk
        #het kan dat er een error optreedt als er geen papier meer is, maar dit moet ik eerst is testen
        print(obj)        
        print_type = obj.get("ticket_type", None)
        
        if print_type is None:
            print("no ticket_type field")
            print("ERROR")
            print_status.put(("alg", "PTYP", "???", -2))
        #hij crashte op deze lijn
        elif print_type == "b":
            print("INFO:", obj['info'])
            print("BESTELLING: ", obj['BST'])
            
            if (obj.get('resend', False)):
                printer_obj.text("+"*10+'\n')
                printer_obj.set(align="center", text_type="b", width=4, height=4)
                printer_obj.text("RESEND\n")
                printer_obj.set(align="left", text_type="normal", width=1, height=1)
                printer_obj.text("+"*10+'\n')
                
            printer_obj.text("TIJD: {}\n".format(obj.get('time', '')))
            printer_obj.text("ID:{:<13}TAFEL:{}\nV:{:<14}HASH:{}\nN:{}\n".format(obj['info']['id'], obj['info']['tafel'], obj['info']['verkoper'], obj['hash'], obj['info']['naam']))
            printer_obj.text("-"*32+"\n")
            for prod in obj['BST']:
                printer_obj.text("{:<28}  {}\n".format(prod, obj['BST'][prod]))
            if obj["opm"].strip():
                print("OPM:", obj['opm'])
                printer_obj.text("-"*32+'\n'+obj["opm"]+'\n')
            printer_obj.text("*"*32)
            printer_obj.cut() #noodzakelijk anders wordt er niets geprint
            
            print_status.put((obj['info']['id'], obj['hash'], obj.get('ptypes', 'no ptypes'), 0))
            
        elif print_type == "r":
            print_kasticket(printer_obj, obj)
            print("geprint")
        elif print_type == "c":
            #send the queue
            print("check")
            #socket operaties gebeuren in een andere thread!
            #via obj["addr"] bekomen we het ip en de poort vinden we gewoon as KV
            #haal eerst x aantal elementen uit de queue(via qsize proberen we ze leeg te maken)
            #daarna picklen we alles en sturen we het door met req="pinfo"
            Thread(target=send_pinfo, args=(obj,), daemon=True).start()
        else:
            print("wrong type!")
        print("\n\n")

    except Exception as e:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        print("line {}: {}".format(str(line), str(e)))
        if LOGGING and not(FILENAME is None):
            with open(FILENAME, "a") as fn:
                fn.write("{}\nline {}: {}\n{}\n\n".format(int(time.time()), line, e, trace_back))
                traceback.print_exc(file=fn)
        
        print_status.put((obj['info']['id'], obj['hash'], obj['ptypes'], -1)) #print error
        
        #could crash
        printer_obj.cut()
    
    finally:    
        return True


def send_pinfo(obj):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg = {'req':"PINFO", "stats":[]}
    temp = []
    for _ in range(print_status.qsize()):
        temp.append(print_status.get())
        msg["stats"].append(temp[-1])
    try:
        s.connect((obj["addr"][0], obj["poort"]))
        s.send(makeMsg({'naam':NAAM}))
        s.send(makeMsg(msg))
    except Exception as e:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        print("line {}: {}".format(str(line), str(e)))
        for i in temp:
            print_status.put(i)
    finally:
        s.close()


#https://github.com/python-escpos/python-escpos/tree/v2.2.0
def print_kasticket(printer_obj, obj):
    try:
        printer_obj.set(align="center", text_type="b", width=4, height=4)
        printer_obj.text("MUSATE\n")
        printer_obj.text("ID: {}\n".format(obj["info"]["ID"]))
        
        printer_obj.set(align="left", text_type="normal", width=1, height=1)
        printer_obj.text("{}\n{}\n\n".format("*"*32, obj['info']['tijd']))
        printer_obj.text("{:<22}  ##  pps \n{}".format("product", "."*32)) #max lengte van het product is 22, indien langer dan eerst product en op volgende lijn aantal
        
        for prod in obj['BST']:
            if obj["BST"][prod] <= 0:
                continue
            elif len(prod)>22:
                printer_obj.text("{:<28} ...\n".format(prod, obj['BST'][prod]))
                printer_obj.text("{:^24}{:<2}X{:>5}\n".format("........", obj['BST'][prod], obj['p_art'].get(prod, "ERR")))
            else:
                printer_obj.text("{:<22}  {:<2}X{:>5}\n".format(prod, obj['BST'][prod], obj['p_art'].get(prod, "ERR")))
        printer_obj.set(text_type="b")
        printer_obj.text("{}\nTOTAAL {:>21} EUR\n".format("-"*32,str(obj['totaal'])))
        #printer_obj.text("TOTAAL {:>22} EUR\n".format(str(obj['totaal'])))
        #printer_obj.text("_"*32+'\n')
        printer_obj.set(align="center", text_type="b")
        printer_obj.text("*****\nBedankt voor uw steun\n*****\nMeer evenementen op musate.be")
        printer_obj.set(align="left", text_type="normal")
        printer_obj.cut()
    except Exception as e:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        print("line {}: {}".format(str(line), str(e)))
    finally:
        return True


class fakePrinter(object):
    PREFIX = "[EP]"
    STANDAARD = {"align":'left', "font":'a', "text_type":'normal', "width":1, "height":1,
                 "density":9, "invert":False, "smooth":False, "flip":False}
    
    def __init__(self, id_vendor, id_product, c, in_end, out_end):
        print(self.PREFIX, "V:{} P:{} I:{} O:{}".format(id_vendor, id_product, c, in_end, out_end))
        print(6*"*")
        self.settings = {}
    
    
    def text(self, _text):
        print(self.PREFIX, _text)
        
    
    def set(self, align='left', font='a', text_type='normal', width=1, height=1,
            density=9, invert=False, smooth=False, flip=False):
        pass
    
    
    @staticmethod
    def close():
        print(fakePrinter.PREFIX, "CLOSED")

    
    def cut(self, **kwargs):
        print(self.PREFIX + "********* CUT *********")


if __name__ == "__main__":
    start_listening()
    