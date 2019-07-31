# -*- coding: utf-8 -*-
import socket
import errno
import pickle
from threading import Thread

HEADERLENGTH = 10
client_socket = None

# Connects to the server
def connect(ip, port, my_username, pwd, error_callback):

    global client_socket

    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to a given ip and port
        client_socket.connect((ip, port))
    except Exception as e:
        # Connection error
        client_socket.close()
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
    client_socket.send(makeMsg(request))
    lengte = int(client_socket.recv(HEADERLENGTH).decode('utf-8'))
    return pickle.loads(client_socket.recv(lengte))


def sendData(request):
    client_socket.send(makeMsg(request))
    

# Starts listening function in a thread
# incoming_message_callback - callback to be called when new message arrives
# error_callback - callback to be called on error
def start_listening(incoming_message_callback, error_callback):
    Thread(target=listen, args=(incoming_message_callback, error_callback), daemon=True).start()

# Listens for incomming messages
def listen(incoming_message_callback, error_callback):
    while True:

        try:
            # Now we want to loop over received messages (there might be more than one) and print them
            while True:

                # Receive our "header" containing username length, it's size is defined and constant
                username_header = client_socket.recv(HEADER_LENGTH)

                # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                if not len(username_header):
                    error_callback('Connection closed by the server')

                # Convert header to int value
                username_length = int(username_header.decode('utf-8').strip())

                # Receive and decode username
                username = client_socket.recv(username_length).decode('utf-8')

                # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')

                # Print message
                incoming_message_callback(username, message)
        
        except IOError as e:
            # This is normal on non blocking connections - when there are no incoming data error is going to be raised
            # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
            # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
            # If we got different error code - something happened
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                error_callback('Reading error: {}'.format(str(e)))
                #sys.exit()
    
            # We just did not receive anything
            continue
        

        except Exception as e:
            # Any other exception - something happened, exit
            error_callback('Reading error: {}'.format(str(e)))