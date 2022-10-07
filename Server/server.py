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
    database = load_database()

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
                else:
                    connectionSocket.send("n\nPlease select the operation:\n1) View uploaded files' information\n2) Upload a file \n3) Terminate the connection\nChoice:".encode("ascii"))
                    print("username good")
                while 1:
                    operation = connectionSocket.recv(2048).decode("ascii")

                    if (operation == '1'):
                        view_files(database, connectionSocket)
                    elif (operation == '2'):
                        upload(connectionSocket, database)
                    elif (operation == '3'):
                        #connectionSocket.close()
                        #KEEP SERVER SOCKET OPEN
                        break
                    else:
                        connectionSocket.send("Invalid Input".encode('ascii'))


            except socket.error as e:
                print('An error occured:',e)
                connectionSocket.close()
                serverSocket.close()
                sys.exit(1)

            connectionSocket.close()


    except socket.error as e:
        print('An error occured:',e)
        connectionSocket.close()
        serverSocket.close()
        sys.exit(1)

    except KeyboardInterrupt:
            #connectionSocket.close()
            serverSocket.close()
            sys.exit(1)


#Create and bind server socket, returns serverSocket object
def connect():

    #Server Port
    serverPort = 13006

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



def view_files(database, connectionSocket):

    output = "Name \tSize (Bytes) \tUpload Date and time\n"



    for file in database:
        output = output + f"{file:<13}{database[file]['size']:<13}{database[file]['time']:<13}"

    try:
        connectionSocket.send(output.encode("ascii"))

    except socket.error as e:
        print('An error occured:',e)
        connectionSocket.close()
        serverSocket.close()
        sys.exit(1)


def upload(connectionSocket, database):

    try:

        connectionSocket.send("Please provide the file name:".encode("ascii"))

        file_name, file_size = connectionSocket.recv(2048).decode("ascii").split("\n")

        connectionSocket.send(f"OK{file_size}".encode("ascii"))

        data = connectionSocket.recv(2048)
        while data:
            with open(file_name, 'wb') as f:
                f.write(data)
            data = connectionSocket.recv(2048)

        with open("Database.json") as f:
            database = json.load(f)

        database[file_name] = {"size": file_size, "time": datetime.time()}

        with open("Database.json", 'wb') as f:
            json.dump(database, f)






    except socket.error as e:
        print("Error Binding Socket: ", e)
        connectionSocket.close()
        sys.exit(1)


def load_database():

    with open("Database.json") as f:
        data = json.load(f)

    return data

def update_database(database):

    with open("Database.json", "w") as f:
        json.dump(database, f)







main()
