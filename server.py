"""
Eric Carstensen - 3070801
CMPT 361 - AS01
Lab 2
"""

import socket
import sys

def main():
    contacts = {}

    serverSocket = connect()
    try:
        while 1:
            try:
                connectionSocket, addr = serverSocket.accept()
                #print(addr, " Has Connected to Socket: ", connectionSocket)

                while 1:
                    operation = connectionSocket.recv(2048).decode('ascii')

                    if (operation == '1'):
                        add_contact(connectionSocket, contacts)
                    elif (operation == '2'):
                        search(connectionSocket, contacts)
                    elif (operation == '3'):
                        #connectionSocket.close()
                        break
                    else:
                        connectionSocket.send("Invalid Input".encode('ascii'))


            except socket.error as e:
                print('An error occured:',e)
                connectionSocket.close()
                serverSocket.close()
                sys.exit(1)

            connectionSocket.close()


    except KeyboardInterrupt:
            #connectionSocket.close()
            serverSocket.close()
            sys.exit(1)


#Create and bind server socket, returns serverSocket object
def connect():

    #Server Port
    serverPort = 13000

    #Create socket using IPv4 and TCP protocols
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Error Creating Socket: ", e)
        sys.exit(1)

    #Bind Server Socket to chosen port
    try:
        serverSocket.bind(('', serverPort))
    except socket.error as e:
        print("Error Binding Socket: ", e)
        sys.exit(1)

    #Set connection queue to max 1
    serverSocket.listen(1)

    #return serverSocket object
    return serverSocket








main()
