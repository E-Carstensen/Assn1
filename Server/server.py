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
    serverSocket = create_socket()

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
                connectionSocket.send("""\n\nPlease select the operation:
1) View uploaded files' information\n2) Upload a file
3) Terminate the connection\nChoice:""".encode("ascii"))


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

        finally:
                #connectionSocket.close()
                serverSocket.close()
                sys.exit(1)

        connectionSocket.close()





#Create and bind server socket, returns serverSocket object
def create_socket():

    #Server Port
    serverPort = 13037

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

    output = "Name \t\tSize (Bytes) \t\tUpload Date and time\n"

    database = load_database()

    for file in database:
        output = output + f"{file:<18}{database[file]['size']:<18}{database[file]['time']:<13}\n"

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

        file = connectionSocket.recv(2048).decode("ascii").split("\n")
        file_name = file[0]
        file_size = file[1]

        connectionSocket.send(f"OK{file_size}".encode("ascii"))
        size = 0
        with open(file_name, 'wb') as f:
            while 1:
                data = connectionSocket.recv(2048)
                size += len(data)
                if data == b"DONE":
                    break
                f.write(data)

                if len(data) < 2048:
                    break


        database = load_database()

        database[file_name] = {"size": file_size, "time": str(datetime.time())}

        update_database(database)







    except socket.error as e:
        print("Error Binding Socket: ", e)
        connectionSocket.close()
        sys.exit(1)

    except exception as e:
        print(e)

def load_database():

    with open("Database.json", 'r') as f:
        data = json.load(f)

    return data

def update_database(database):

    with open("Database.json", "w") as f:
        json.dump(database, f)







main()
