# -*- coding: utf-8 -*-
#gebaseerd op
#https://pythonprogramming.net/server-chatroom-sockets-tutorial-python-3/
import socket
import sys
import select
import queue


HEADERLENGTH = 10
IP = "0.0.0.0"
POORT = 9000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, POORT))

server_socket.listen()

#lijst met sockets
sockets_list = [server_socket]
connecties = {} #socket:naam --> komt van allereerste bericht dat we zullen ontvangen

print("Aan het luisteren voor connecties op: {0}:{1}".format(IP, POORT))

#verwerkt de data
def handles_message(client_socket):
    try:
        message_header = client_socket.recv(HEADERLENGTH)
        
        #connection closed
        if not len(message_header):
            return 0
        
        lengte = message_header.decode("utf-8")
        data = client_socket.recv(lengte)
        
        return {"header":message_header, "data":data}
    except:
        return 0

while True:
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

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()

            #ontvang
            #TODO
            
            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)

            # Also save username and username header
            #connecties[client_socket] = user
            
            #print mss ook de naam
            print('Accepted new connection from {}'.format(client_address))

        # Else existing socket is sending a message
        else:

            # Receive message
            message = handles_message(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print("Connectie gesloten!")
                
                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                #del connecties[notified_socket]
                continue

            # Get user by notified socket, so we will know who sent the message
            #user = connecties[notified_socket]

            #print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        #del connecties[notified_socket]
    
    
