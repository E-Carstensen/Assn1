"""
Eric Carstensen - 3070801
CMPT 361 - AS01
Assignment 1
"""

import socket
import sys

#Main client loop, calls menu to take user choice in operation then calls
#matching subroutine
def main():
    #initiate server connection
    clientSocket = connect()
    try:
        while (1):
            #Call menu funtion to get user choice and send to server
            option = menu()
            clientSocket.send(option.encode('ascii'))

            #run corresponding subroutine
            if (option == '1'):
                add_contact(clientSocket)
            elif(option == '2'):
                search(clientSocket)
            elif(option == '3'):
                disconnect(clientSocket)
                break

    #Catch errors in clientSocket creation and handling
    except socket.error as e:
        print("Error:", e)
        clientSocket.close()
        sys.exit(1)

    #If loop is broken, close connection and exit
    clientSocket.close()
    sys.exit(1)



#Displays main menu options, takes input and returns string if input is valid
def menu():

    #Print menu options and take user input
    option = input("""Please select the operation
1)Add a new entry
2)Search
3)Terminate the connection

Choice: """)

    #If input is one of options and only 1 character
    if(option in "123" and len(option) == 1):
        return option
    else:
        #The input is not one of the options or is more than 1 character
        print("Input Not Recognized")
        #Recursively call menu function
        return menu()




#Take server address from user, initiate socket, and connect to server
#Returns clientSocket object
def connect():
    #Default server information
    serverName = '127.0.0.1'
    serverPort = 13000

    #Take server name from user
    temp = input("Enter the server name or IP address: ")
    if (len(temp) != 0):
        #If user does not enter an address, use default serverName
        serverName = temp

    #Attempt to create client socket with IPv4 and TCP protocols
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Error in client socket creation:',e)
        sys.exit(1)

    #Attempt to connect clientSocket to given server name and port 13000
    try:
        clientSocket.connect((serverName, serverPort))
        print("Welcome to the online phone book. \n")
    except socket.error as e:
        print("Error:", e)
        clientSocket.close()
        sys.exit(1)

    #return initiated clientSocket object
    return clientSocket


#Search subroutine, sends search term then recieves and prints formatted result
def search(clientSocket):
    #recieve prompt from server
    message = clientSocket.recv(2048).decode('ascii')
    #take search term as input from user
    val = input(message)
    #send server search term
    clientSocket.send(val.encode('ascii'))
    #recieve formatted string of all contacts with matching info
    result = clientSocket.recv(2048).decode('ascii')
    #print result to user
    print(result)

#Add contact subroutine, takes prompts from server and sends new contact info
def add_contact(clientSocket):
    #recieve "Enter Name" prompt
    message = clientSocket.recv(2048).decode('ascii')
    #take new contact name info from user
    name = input(message)
    #send name of new contact to server
    clientSocket.send(name.encode('ascii'))
    #recieve "Enter Number" prompt
    message = clientSocket.recv(2048).decode('ascii')
    #take new number info from user
    num = input(message)
    #send number for new contact to server
    clientSocket.send(num.encode('ascii'))


#Terminate the connection with the server
def disconnect(clientSocket):
    #Send the server the disconnect operation
    clientSocket.send('3'.encode('ascii'))
    #Close the socket
    clientSocket.close()
    #Print message to user to inform the connection has been closed
    print("Connection Terminated")
    return


if __name__ == '__main__':
    main()
