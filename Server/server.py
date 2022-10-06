"""
Eric Carstensen - 3070801
CMPT 361 - AS01
Assignment 1
"""

import socket
import sys
import json
import os
import datetime

def main():
    contacts = {}

    #Creates the server socket and starts listening
    serverSocket = connect()

    try:
        while 1:
            try:
                #Accept connection
                connectionSocket, addr = serverSocket.accept()
                #Send new connection welcome message and prompt for username
                connectionSocket.send("Welcome to our system.\nEnter your username: ".encode("ascii"))
                #Recieve username from user
                user_name = connectionSocket.recv(2048).decode('ascii')

                if (user_name != "user1"):
                    connectionSocket.send("“Incorrect username. Connection Terminated.".encode("ascii"))
                    connectionSocket.close()
                    continue

                connectionSocket.send("n\nPlease select the operation:\n1) View uploaded files' information\n2) Upload a file \n3) Terminate the connection\nChoice:".encode("ascii"))

                while 1:

                    operation = connectionSocket.recv(2048).decode("ascii")

                    if (operation == '1'):
                        view_files()
                    elif (operation == '2'):
                        upload(connectionSocket, contacts)
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



def view_files():


def upload():





main()
