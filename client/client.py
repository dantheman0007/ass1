# CLIENT
# TODO: properly exit program, hash message 
import socket
import threading
import sys
import os
import signal
import configparser

import login
import main
from os import path
from tkinter import *

class Client:

    SERVER_NAME = "196.47.216.151"
    SERVER_PORT = 9999

    def __init__(self, parent) -> None:
        self.parent = parent
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind(("196.42.127.35", 2789))
        
        if not path.exists(".config"):
            config = configparser.ConfigParser()

            config["SESSION_INFO"] = {
                "user_id": ""
            }


            with open(".config", "w") as configfile:
                config.write(configfile)


        listenMessage = threading.Thread(target=self.listenForMessage, )
        listenMessage.start()

        

        

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(".config")

        self.user_id = config["SESSION_INFO"]["user_id"]
        pass
        

    def createHeader(self, flag, message, recipientUser):

        if flag == "LOGIN":
            return flag + "`" + self.user_id

        elif flag == "SEND":
            return flag + "`" + self.user_id + recipientUser + message
            #would probably change recipientUser to the chatID

        elif flag == "CHAT":
            return flag + "`" + self.user_id + recipientUser
            # recipientUser would be a list of users for a groupchat

        elif flag == "QUIT":
            return flag + "`" + self.user_id

        '''
        # TODO implement protocol into header'''


    def listenForMessage(self):
   
        while True:
            receivedMessage, serverAddress = self.client_socket.recvfrom(2048)

            self.message_received(receivedMessage.decode())
            
            print(receivedMessage.decode())


    def message_received(self, message):
        print("Hello")
        # DO somethinf to print ot the screen
        chat_id = "167831c0-be28-4689-b040-49048118956e"
        payload = {"message_id": "abc",
         "msg_content": message,
          "timestamp": "",
           "from_id": "MRRJUL007"
           }
        
        self.parent.chat_screens[chat_id].write_message(payload)
        
        pass


'''
serverName = "127.0.0.1"
serverPort = 9999 
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
'''

username = ""
#recipientUser= ""

# takes in input message from user
# should probably be corrected to createDatagram() after correct header implementation
def createHeader(flag, message, recipientUser):

    if flag == "LOGIN":
        return flag + "`" + username

    elif flag == "SEND":
        return flag + "`" + username + recipientUser + message
        #would probably change recipientUser to the chatID

    elif flag == "CHAT":
        return flag + "`" + username + recipientUser
        # recipientUser would be a list of users for a groupchat

    elif flag == "QUIT":
        return flag + "`" + username

    '''
    # TODO implement protocol into header'''
'''
# runs in own thread
def listenForMessage():
   
    while True:
        receivedMessage, serverAddress = clientSocket.recvfrom(2048)
        #print(f"{recipientUser} > {receivedMessage.decode('utf-8')}")
        print(receivedMessage.decode())
   '''     
# # runs in second thread
# def listenForInput(): # from user keyboard

#     #recipientUser= input(f"Who would you like to talk to? \n{username}> ")
#     inChat= True
    
#     while inChat:
#         print("Enter one of the following keywords:")
#         print("CHAT - to start a chat")
#         print("SEND - to send a message")
#         print("QUIT - to logout")
#         usrmessage= input(f"{username} > ")
#         #recipientUser= input(f"Who would you like to talk to? \n{username}> ")

#         if usrmessage == "QUIT": # user disconnecting
#             clientSocket.sendto(createHeader("QUIT", "", "").encode('utf-8'),(serverName,serverPort))
#             #change online to false
#             print("Signing out...")
#             #clientSocket.close()
#             quit()
#             #inChat=False
            
#             #return
#             # TODO properly exit program (can do it when gui done?)
#             # try:
#             #    os.kill(os.getpid(), signal.SIGINT)
#             # need to close client socket
#             # except:
                

#         elif usrmessage== "get": # not used at the moment, need to wait for how protocol is done
#             try:
#                 receivedMessage, serverAddress = clientSocket.recvfrom(2048)
#                 print(receivedMessage.decode('utf-8'))
#             except:
#                 print("timed out")
        
#         elif usrmessage == "CHAT":
#             users = input("Enter list of users separated by a space: ")
#             message = createHeader("CHAT","", users)
#             clientSocket.sendto(message.encode('utf-8'),(serverName,serverPort))
        
#         elif usrmessage == "SEND": # send message to server
#             recipientUser= input(f"Who would you like to talk to? \n{username}> ")
#             usrmessage = input(f"Input message to send to {recipientUser}: ")
#             message = createHeader("SEND",usrmessage, recipientUser)
            
            
#             clientSocket.sendto(message.encode('utf-8'),(serverName,serverPort))
#     return


# def main():

#     initialMessage= createHeader("LOGIN", "", "").encode('utf-8') # login in, will add the user to the database if not already in
#         # TODO get feedback from server if recipient is  valid

#     clientSocket.sendto(initialMessage, (serverName, serverPort))
#     receivedMessage, serverAddress = clientSocket.recvfrom(2048)
#     print(receivedMessage.decode())
#     listenMessage = threading.Thread(target=listenForMessage, )
#     listenMessage.start()
    
#     listenInput = threading.Thread(target=listenForInput,)
#     listenInput.start()

   


if __name__ == "__main__":
    pass
