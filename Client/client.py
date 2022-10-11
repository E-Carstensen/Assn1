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
        #Recieve prompt for username from server
        message = connectionSocket.recv(2048).decode("ascii")
        #Take username from user
        user_name = input(message)

        #DEBUG: Allows developer to login quicker for testing
        #if (len(user_name) == 0):
        #    user_name = "user1"

        #Send username
        connectionSocket.send(user_name.encode("ascii"))


        while (1):
            #Recieve response from server, either menu options or incorrect username
            main = connectionSocket.recv(2048).decode("ascii")

            #If server rejects connection, close socket
            if ("Incorrect username" in main):
                print(main)
                connectionSocket.close()
                return


            #Call menu funtion to get user choice and send to server
            option = menu(main)
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
def menu(main):
    #Print menu options and take user input
    option = input(main)

    #If input is one of options and only 1 character
    if(option in "123" and len(option) == 1):
        return option
    else:
        #The input is not one of the options or is more than 1 character
        print("Input Not Recognized")
        #Recursively call menu function
        return menu(main)




#Take server address from user, initiate socket, and connect to server
#Returns connectionSocket object
def connect():
    #Default server information
    serverName = '127.0.0.1'
    serverPort = 13000

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
    #Recieve "enter file name" prompt
    message = connectionSocket.recv(2048).decode("ascii")

    #While file name not found, take input from user
    file_name = input(message)
    while 1:
        try:
            file_size = os.stat(file_name).st_size
            break
        except:
            print("File Not Found")
            file_name = input(message)

    #Combine file name and size to string and send to server
    message = file_name + "\n" + str(file_size)
    connectionSocket.send(message.encode("ascii"))

    #Server responds with ACK confirming file name and size
    ack = connectionSocket.recv(2048).decode("ascii")
    print(ack)
    #Read data from specified file
    with open(file_name, 'rb') as f:
        data = f.read()

    #Send all the data to the server
    connectionSocket.sendall(data)
    #Send flag indication the end of the file
    #connectionSocket.send(b"DONE")
    print("Upload process completed")
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
