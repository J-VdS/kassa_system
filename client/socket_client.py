# -*- coding: utf-8 -*-
import socket
import pickle


HEADERLENGTH = 10
client_socket = None
ON_ERR = None

# Connects to the server
def connect(ip, port, my_username, pwd, error_callback):

    global client_socket
    global ON_ERR
    ON_ERR = error_callback

    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to a given ip and port
        client_socket.connect((ip, port))
    except Exception as e:
        # Connection error
        #client_socket.close()
        error_callback('Connection error: {}'.format(str(e)))
        return False

    # Prepare username and header and send them
    # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
    #msg = pickle.dumps({"naam":my_username, "pwd":pwd})
    #msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(makeMsg({"naam":my_username, "pwd":pwd}))
    return True


def disconnect():
    client_socket.close()


def makeMsg(msg):
    msg = pickle.dumps(msg)
    msg_header = f"{len(msg):<{HEADERLENGTH}}".encode('utf-8')  
    return msg_header + msg


#def receiveMsg():
#    lengte = int(client_socket.recv(HEADERLENGTH).decode('utf-8'))
#    return pickle.loads(client_socket.recv(lengte))
    
    
def requestData(request):
    try:
        client_socket.send(makeMsg(request))
        lengte = int(client_socket.recv(HEADERLENGTH).decode('utf-8'))
        return pickle.loads(client_socket.recv(lengte))
    except socket.error as e:
        if e.errno == 10053:
            ON_ERR('Server is gesloten. Je kan je bestelling terug inladen via de BACK UP knop.')
            return -1
        else:
            ON_ERR('Connection error [RD]: {}'.format(str(e)))
            return -1
    except Exception as e:
        ON_ERR('Connection error [RD]: {}'.format(str(e)))
        return -1


def sendData(request):
    '''
    return waarden:
        -1: Verbinding verbroken en het info scherm wordt weer getoont
        {}: bevat oa {status}
    
    '''
    try:
        #client_socket.send(makeMsg({"req":"PING"})) #minstens 2 mislukte calls voor dat connectie wordt gedetecteerd als verbroken
        client_socket.send(makeMsg(request))
        print(client_socket)
    except Exception as e:
        ON_ERR('Verbinding verbroken...\nConnection error: {}'.format(str(e)))
        return -1
    
    
def listenData():
    #zet de timeout op 5 seconden
    try:
        client_socket.settimeout(5)
        lengte = int(client_socket.recv(HEADERLENGTH).decode('utf-8'))
        client_socket.settimeout(None)
        return pickle.loads(client_socket.recv(lengte))
    except socket.timeout: # Exception as e:
        #ON_ERR('Verbinding verbroken...\nGa naar de kassa om te controleren of je bestelling aankwam...\nConnection error: {}'.format(str(e)))
        client_socket.settimeout(None)
        return 1
    except Exception as e:
        ON_ERR('Verbinding verbroken...\nGa naar de kassa om te controleren of je bestelling aankwam...\nConnection error: {}'.format(str(e)))
        return -2