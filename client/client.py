# CLIENT
# TODO: properly exit program, hash message 
import socket
import threading
import sys
import os
import signal
import configparser
from os import path
import json
from tkinter import *

from flask import request


class Client:


    def __init__(self, parent) -> None:
        self.parent = parent
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._is_running= True
        host_name = socket.gethostname()
        client_ip = socket.gethostbyname(host_name)

        self.login()

        listenMessage = threading.Thread(target=self.listenForMessage, )
        listenMessage.start()
        
    def stop(self):
        self._is_running = False

    def create_request(self, flag, **kwargs):
        header = "`".join([flag, self.parent.user_id])
        
        payload = {}

        for key, value in kwargs.items():
            payload[key] = value

        payload_str = json.dumps(payload)

        request = "`".join([header, payload_str])

        return request

    def send_request(self, request):
        print("Sending: "+request)
        self.client_socket.sendto(request.encode("utf-8"), (self.parent.SERVER_NAME, self.parent.SERVER_PORT))


    def send_message(self, message, chat_id):
        request = self.create_request("SEND", message = message, chat_id = chat_id)

        print("Sending message: " + request)
        self.send_request(request)

    def login(self):
        request = self.create_request("LOGIN")
        self.send_request(request)

    def new_chat(self, users):
        print("Making new chat with: ", users)
        request = self.create_request("CHAT", receivers = users)
        self.send_request(request)
        pass

    def refresh_chats(self):
        pass

    def log_out(self, ):
        print("Logging off.") 
        request = self.create_request("QUIT")
        self.send_request(request)
        self.stop()

    def get_messages(self, chat_id):
        request = self.create_request("HISTORY", chat_id = chat_id)
        self.send_request(request)

    def listenForMessage(self):
        while (self._is_running):
            receivedMessage, serverAddress = self.client_socket.recvfrom(1000000)
            print(receivedMessage.decode())
            self.decode_message(receivedMessage.decode())
        return
            
            
    def decode_message(self, response):

        response = response.split("`")
        flag = response[0]
        sender = response[1]
        msg_content= response[2]

        if flag == "CHATS":
            self.parent.chats = json.loads(msg_content)
            print("Parent chats:",  self.parent.chats)

        elif flag == "SEND":
            payload = json.loads(msg_content)
            self.parent.chat_screens[payload["chat_id"]].write_message(payload)
        
        elif flag == "HISTORY":
            payload = json.loads(msg_content)

            self.parent.open_chat_screen(payload)

        pass

    def message_received(self, message):
        # DO somethinf to print ot the screen
        chat_id = "167831c0-be28-4689-b040-49048118956e"
        payload = {"message_id": "abc",
         "msg_content": message,
          "timestamp": "",
           "from_id": "MRRJUL007"
           }
        self.parent.chat_screens[chat_id].write_message(payload)
        
        pass
    
    def myHash(self, text):
        hash=0
        for ch in text:
            hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
        return hash
'''
serverName = "127.0.0.1"
serverPort = 9999 
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
'''

# #recipientUser= ""


# # takes in input message from user
# # should probably be corrected to createDatagram() after correct header implementation
# def createHeader(flag, message, recipientUser):

#     if flag == "LOGIN":
#         return flag + "`" + username

#     elif flag == "SEND":
#         return flag + "`" + username + recipientUser + message
#         #would probably change recipientUser to the chatID

#     elif flag == "CHAT":
#         return flag + "`" + username + recipientUser
#         # recipientUser would be a list of users for a groupchat

#     elif flag == "QUIT":
#         return flag + "`" + username


# '''
# # runs in own thread
# def listenForMessage():
   
#     while True:
#         receivedMessage, serverAddress = clientSocket.recvfrom(2048)
#         #print(f"{recipientUser} > {receivedMessage.decode('utf-8')}")
#         print(receivedMessage.decode())
#    '''     
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
                

              
        #elif usrmessage == "CHAT":
        #    users = input("Enter list of users separated by a space: ")
         #   message = createHeader("CHAT","", users)
          #  clientSocket.sendto(message.encode('utf-8'),(serverName,serverPort))
          
          
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
    


if __name__ == "__main__":
    pass
