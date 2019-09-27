# -*- coding: utf-8 -*-
#gebaseerd op
#https://pythonprogramming.net/server-chatroom-sockets-tutorial-python-3/
import socket
import select
import pickle
import database
import func
#error handling
import sys

#RUN_SERVER = True

HEADERLENGTH = 10 #10
IP = "0.0.0.0"
POORT = 1740
RUN = True
ACCEPT = True
PRINTERS = [] #(ip, poort, [type,])

EDIT_ID = None

#verwerkt de data
def handles_message(client_socket):
    try:
        message_header = client_socket.recv(HEADERLENGTH)
        
        #connection closed
        if not len(message_header):
            return 0
        lengte = int(message_header.decode("utf-8"))
        data = client_socket.recv(lengte) #pickled-data
        return pickle.loads(data) #dict bevat request en eventuele data
    except:
        return 0
    

def get_products(db_io):
    products = pickle.dumps(func.sort_by_type(database.getAllProductClient(db_io)))
    msg = f"{len(products):<{HEADERLENGTH}}".encode("utf-8") + products
    return msg


def get_host_ip():   
    return socket.gethostbyname(socket.gethostname())
    

def TriggerSD():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1',POORT))
    s.send("{:<{}}".format(0,HEADERLENGTH).encode("utf-8")) #eig fout
    s.close()
    

def makeMsg(msg):
    msg = pickle.dumps(msg)
    msg_header = f"{len(msg):<{HEADERLENGTH}}".encode('utf-8')  
    return msg_header + msg
    

def printer_bestelling(bestelling):
    producten = bestelling['BST']
    info = bestelling['info']
    opm = bestelling['opm']
    for ip, poort, types in PRINTERS:
        b = {}
        for t in types:
            b.update(producten.get(t, {}))
        msg = makeMsg({'info':info, 'opm':opm, 'BST':b})
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, poort))
            s.send(msg)
        except Exception as e:
            #verwijder de printer uit de lijst van connecties, en geef popup
            print("Error:", e)
        finally:
            s.close()
            

def printer_test(ip, poort):
    msg = makeMsg({'info':{'id':0, 'tafel':-1, 'naam':'KASSA', 'verkoper':'KASSA'},
                   'opm':"DIT is een test, geen actie nodig...",
                   'BST':{}})
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, poort))
        s.send(msg)
    except Exception as e:
        print("Error:", e)
    finally:
        s.close()
        
        
def sluit_printers():
    msg = makeMsg({"STOP":True})
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for ip, poort, _ in PRINTERS:
        try:
            s.connect((ip, poort))
            s.send(msg)
        except Exception as e:
            #verwijder de printer uit de lijst van connecties, en geef popup
            print("Error:", e)
        finally:
            s.close()


def start_listening(db, crash_func, update_func, password=None, get_items=None, store_order=None):
    #we zullen een connectie proberen te openen met de db om daar de producten op te vragen,
    #en de bestellingen in op te slaan.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, POORT))
    
    server_socket.listen()
    
    #lijst met sockets
    sockets_list = [server_socket]
    connecties = {} #socket:naam --> komt van allereerste bericht dat we zullen ontvangen
    
    db_io = database.OpenIO(db)
    
    try:
        #print("Aan het luisteren voor connecties op: {0}:{1}".format(IP, POORT))
        while RUN:
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
                if notified_socket == server_socket:
                    try:
                        # Accept new connection
                        # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                        # The other returned object is ip/port set
                        client_socket, client_address = server_socket.accept()
            
                        #ontvang
                        lengte = int(client_socket.recv(HEADERLENGTH).decode("utf-8"))
                        if not lengte:
                            client_socket.close()
                            continue
                        data = pickle.loads(client_socket.recv(lengte))
                        '''
                        if password:
                            if data["pwd"] != password:
                                #laat weten dat het een verkeerd passwoord is
                                client_socket.close()
                                continue #skipt de rest 
                        '''
                        # Add accepted socket to select.select() list
                        sockets_list.append(client_socket)
                                
                        # Also save username and username header
                        connecties[client_socket] = data['naam']
                        
                        #print mss ook de naam
                        print('Accepted new connection from {}:{}'.format(client_address, data['naam']))
                    #vermijd random bytes naar de kassa
                    except Exception as e:
                        print("NetwerkError: ", e)
                        client_socket.close()
        
                # Else existing socket is sending a message
                else:                    
                    # Receive message
                    message = handles_message(notified_socket)
                    
                    # Get user by notified socket, so we will know who sent the message
                    user = connecties[notified_socket]
                    
                    # If False, client disconnected, cleanup
                    if not(message):
                        print(f"Connectie met {user} gesloten!")
                        #gebruik conn.close() om de connectie te sluiten!
                        # Remove from list for socket.socket()
                        sockets_list.remove(notified_socket)
        
                        # Remove from our list of users
                        del connecties[notified_socket]
                        notified_socket.close() #mss ni nodig - close connection
                        
                        continue

                    if message['req'] == "GET":
                        notified_socket.send(get_products(db_io))
                        print(f"[SERVER][GET]{user} vroeg alle producten op")
                    elif message['req'] == "BST":
                        #verwerk bestelling
                        #{bestelling:{BST:{type:{}}}
                        best = {}
                        for d in message['bestelling']['BST'].values():
                            best.update(d)
                        global EDIT_ID
                        while EDIT_ID == message['bestelling']['info']['id']:
                            pass
                        EDIT_ID = message['bestelling']['info']['id']
                        ret = database.addBestelling(db_io, message['bestelling']['info'], best)
                        #stuur valid en goed ontvangen naar client
                        if ret == 1:
                            #herlaad de rekeningen
                            update_func(db_io)
                        EDIT_ID = None
                        
                        #stuur naar printer
                        printer_bestelling(message['bestelling'])
                        #stuur succes, gelukt naar kassa
                    elif message['req'] == "MSG":
                        pass
        
            # It's not really necessary to have this, but will handle some socket exceptions just in case
            for notified_socket in exception_sockets:
        
                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)
        
                # Remove from our list of users
                #del connecties[notified_socket]
    except Exception as e:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        print(f"line {line}: {str(e)}")
        crash_func()
    finally:
        for s in sockets_list:
            if sockets_list != server_socket:
                s.close()
        print("DB connection closed")
        database.CloseIO(db_io)
        print("SERVER closed")
        server_socket.close()
        