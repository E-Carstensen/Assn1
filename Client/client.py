"""
Eric Carstensen - 3070801
CMPT 361 - AS01
Assignment 1

"""

import socket
import sys
import os
import datetime

#Main client loop, calls menu to take user choice in operation then calls
#matching subroutine
def main():
    #initiate server connection
    connectionSocket = connect()
    try:
        message = connectionSocket.recv(2048).decode("ascii")

        user_name = input(message)

        if (len(user_name) == 0):
            user_name = "user1"

        connectionSocket.send(user_name.encode("ascii"))

        #Recieve response from server
        message = connectionSocket.recv(2048).decode("ascii")

        if ("Incorrect username" in message):
            print(message)
            connectionSocket.close()
            return

        while (1):
            #Call menu funtion to get user choice and send to server
            option = menu(message)
            print(option)
            connectionSocket.send(option.encode('ascii'))

            #run corresponding subroutine
            if (option == '1'):
                view_files(connectionSocket)
            elif(option == '2'):
                upload(connectionSocket)
            elif(option == '3'):
                disconnect(connectionSocket)
                break

    #Catch errors in connectionSocket creation and handling
    except socket.error as e:
        print("Error:", e)
        connectionSocket.close()
        sys.exit(1)

    #If loop is broken, close connection and exit
    connectionSocket.close()
    sys.exit(1)



#Displays main menu options, takes input and returns string if input is valid
def menu(message):
    #Print menu options and take user input
    option = input(message)

    #If input is one of options and only 1 character
    if(option in "123" and len(option) == 1):
        return option
    else:
        #The input is not one of the options or is more than 1 character
        print("Input Not Recognized")
        #Recursively call menu function
        return menu(message)




#Take server address from user, initiate socket, and connect to server
#Returns connectionSocket object
def connect():
    #Default server information
    serverName = '127.0.0.1'
    serverPort = 13037

    #Take server name from user
    temp = input("Enter the server name or IP address: ")
    if (len(temp) != 0 and "localhost" not in temp):
        #If user does not enter an address, use default serverName
        serverName = temp

    #Attempt to create client socket with IPv4 and TCP protocols
    try:
        connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Error in client socket creation:',e)
        sys.exit(1)

    #Attempt to connect connectionSocket to given server name and port 13000
    try:
        connectionSocket.connect((serverName, serverPort))
    except socket.error as e:
        print("Error:", e)
        connectionSocket.close()
        sys.exit(1)

    #return initiated connectionSocket object
    return connectionSocket



def view_files(connectionSocket):

    message = connectionSocket.recv(2048).decode('ascii')
    print(message)

#Terminate the connection with the server
def disconnect(connectionSocket):
    #Send the server the disconnect operation
    connectionSocket.send('3'.encode('ascii')) #change to terminate keyword
    #Close the socket
    connectionSocket.close()
    #Print message to user to inform the connection has been closed
    print("Connection Terminated")
    return


def upload(connectionSocket):
    #USE SEND all function of SOCKET
    message = connectionSocket.recv(2048).decode("ascii")

    file_name = input(message)

    try:
        file_size = os.stat(file_name).st_size
    except:
        print("File Not Found")
        upload(connectionSocket)
        return

    message = file_name + "\n" + str(file_size)
    connectionSocket.send(message.encode("ascii"))

    ack = connectionSocket.recv(2048).decode("ascii")
    print(ack)

    with open(file_name, 'rb') as f:
        data = f.read()

    connectionSocket.sendall(data)
    connectionSocket.send(b"DONE")

    return

'''
    with open(file_name, 'rb') as f:

        while True:

            data = f.read(1024)

            if not data:
                break
            print("Sending...")
            connectionSocket.sendall(data)

'''





if __name__ == '__main__':
    main()
