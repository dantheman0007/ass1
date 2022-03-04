# CLIENT

import socket
import threading
import sys
import os
import signal

serverName = "127.0.0.1"
serverPort = 9999 
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


username= input("Username (9 digit student number): \n")
recipientUser= input(f"Who would you like to talk to? \n{username}> ")

def createHeader(message):
    # return "START"+username + recipientUser
    if not message: # first message to server to see if recipientUser is in database
        return username + recipientUser
    else:
        return username+recipientUser+ message
        #return username+recipientUser+" START"+ message

def listenForMessage():
   
    while True:
        print("listening")
        receivedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(f"{recipientUser} > {receivedMessage.decode('utf-8')}")


def listenForInput():

    inChat= True
    
    while inChat:
        usrmessage= input(f"{username} >")
        if usrmessage == "quit":
            clientSocket.sendto(createHeader("QUIT").encode('utf-8'),(serverName,serverPort))
            print("Signing out...")
            inChat=False
            return
            # try:
            #    os.kill(os.getpid(), signal.SIGINT)
            # except:
                

        elif usrmessage== "get":
            try:
                receivedMessage, serverAddress = clientSocket.recvfrom(2048)
                print(receivedMessage.decode('utf-8'))
            except:
                print("timed out")
        else:
            message = createHeader(usrmessage)
            clientSocket.sendto(message.encode('utf-8'),(serverName,serverPort))
    return


def main():

    initialMessage= createHeader("").encode('utf-8')
        # get feedback from server if recipient is  valid

    clientSocket.sendto(initialMessage, (serverName, serverPort))

    recipientUserStatus, serverAddress = clientSocket.recvfrom(2048)

    print(recipientUserStatus.decode('utf-8'))

    
    listenMessage = threading.Thread(target=listenForMessage, )
    listenMessage.start()
    
    listenInput = threading.Thread(target=listenForInput,)
    listenInput.start()

    '''
    while inChat:
        usrmessage= input(f"{username} >")
        if usrmessage == "quit":
            clientSocket.sendto(createHeader("QUIT").encode('utf-8'),(serverName,serverPort))
            print("Signing out...")
            inChat(False)
            break
            #sys.exit("Disconnected")
            # try:
            #    os.kill(os.getpid(), signal.SIGINT)
            # except:
                

        elif usrmessage== "get":
            try:
                receivedMessage, serverAddress = clientSocket.recvfrom(2048)
                print(receivedMessage.decode('utf-8'))
            except:
                print("timed out")
        else:
            message = createHeader(usrmessage)
            clientSocket.sendto(message.encode('utf-8'),(serverName,serverPort))
    sys.exit(0)
    # clientSocket.close()
    '''


if __name__ == "__main__":
    main()
