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
    #Read database from JSON file
    database = load_database()

    #Creates the server socket and starts listening
    serverSocket = create_socket()

    #Main loop - Continues acception connections
    while 1:
        try:
            #Accept connection
            connectionSocket, addr = serverSocket.accept()

            #Take and compare username, if incorrect close connection and await next
            if login(connectionSocket) == False:
                continue

            #Second Loop - Allows multiple acction per connection
            while 1:
                #Send Main menu prompt to user
                connectionSocket.send("""\n\nPlease select the operation:
1) View uploaded files' information\n2) Upload a file
3) Terminate the connection\nChoice:""".encode("ascii"))

                #Recieve user choice for operation
                operation = connectionSocket.recv(2048).decode("ascii")

                #Run subprotocol depending on user choice
                if (operation == '1'):
                    view_files(database, connectionSocket)
                elif (operation == '2'):
                    upload(connectionSocket, database)
                elif (operation == '3'):
                    #Terminate connection with user
                    break
                else:
                    #If input is not valid
                    connectionSocket.send("Invalid Input".encode('ascii'))



        #Error handling incase of broken connection
        except socket.error as e:
            print('An error occured:',e)
            connectionSocket.close()
            serverSocket.close()
            sys.exit(1)

        #Close connections after user disconnects
        connectionSocket.close()


#Create and bind server socket, returns serverSocket object
def create_socket():

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

#Sends login prompt to client then recieves and compares usernames
#Returns True if username is correct, False otherwise
def login(connectionSocket):

    #Send new connection welcome message and prompt for username
    connectionSocket.send("Welcome to our system.\nEnter your username: ".encode("ascii"))
    #Recieve username from user
    user_name = connectionSocket.recv(2048).decode('ascii')

    #If username is incorrect, send error to client and close connection
    if (user_name != "user1"):
        connectionSocket.send("Incorrect username. Connection Terminated.".encode("ascii"))
        connectionSocket.close()
        return False
    else:
        return True


#Sends a formatted string of database JSON to client
def view_files(database, connectionSocket):
    #Init output string with header
    output = "\nName \t\tSize (Bytes) \t\tUpload Date and time\n"

    #Read database from JSON file
    database = load_database()

    #For each file stored in the databse
    for file in database:
        #Append file info to output string with padding
        output = output + f"{file:<16}{database[file]['size']:<24}{database[file]['time']:<13}\n"

    #Send formatted string to client
    try:
        connectionSocket.send(output.encode("ascii"))

    except socket.error as e:
        print('An error occured:',e)
        connectionSocket.close()
        serverSocket.close()
        sys.exit(1)


#Subprotocol for recieving files from client
#Sends prompt to client for file name, recieves file name and size as 1 string
#Send ACK to client then begins recieving file data
#Breaks when end of file is found, and updates JSON database
def upload(connectionSocket, database):

    try:
        #Send prompt to client for file name
        connectionSocket.send("Please provide the file name:".encode("ascii"))

        #Recieve file name and file size in formatted string
        file = connectionSocket.recv(2048).decode("ascii").split("\n")
        file_name = file[0]
        file_size = file[1]

        #Send ACK to client confiming file size
        connectionSocket.send(f"OK{file_size}".encode("ascii"))

        #Init counter for amount of data recieved
        size = 0

        with open(file_name, 'wb') as f:
            while 1:
                #Recieve 2048 bytes of data
                data = connectionSocket.recv(2048)
                #Increment counter
                size += len(data)
                #If end of file flag reieved, break
                if data == b"DONE":
                    break
                #Write recieved data to file
                f.write(data)

                #If size of data is smaller than buffer, end of file reached
                if len(data) < 2048 or size == file_size:
                    break


        #Get up to date database from JSON file
        database = load_database()

        #Append/Modify entry for file in database
        database[file_name] = {"size": file_size, "time": str(datetime.datetime.now())}

        #Update the JSON file with up to date database object
        update_database(database)

    except socket.error as e:
        print("Error: ", e)
        connectionSocket.close()
        sys.exit(1)

#Reads database JSON file and returns dict object
def load_database():

    with open("Database.json", 'r') as f:
        data = json.load(f)

    return data

#Takes database dict and writes it to JSON file
def update_database(database):

    with open("Database.json", "w") as f:
        json.dump(database, f)





main()
