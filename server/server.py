# SERVER

import socket
import threading
from typing_extensions import dataclass_transform
import models
import db
import sqlalchemy
from datetime import datetime
import json

class Server:

    def __init__(self):
        self.serverPort = 9999 
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initialising server object
        self.serverSocket.bind(("",self.serverPort)) # bind to local host
        self.database = db.DB()
        self.server()


    def myHash(self, text):
        '''
        Hash function that performs a hash on the input string.

        Parameters:
        text (str): the text that the hash function must be performed on.
        '''
        hash = 0
        for ch in text:
            hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
        return str(hash)

    def sendMessage(self,flag, out_message):
        '''
        Method to send a message using the flag and a message object as defined by the models program.
        
        Parameters:
            flag: the flag that shows that the send protocol must be followed
            out_message: message object
        '''    
        
        receivers = out_message.chat_id.split("-") #makes a list of receivers from the chat_id oof the message object
        for user in receivers:
            if user != out_message.from_id: #done so that the sender does not receive their own message
                rec = self.database.get_record_from_pk(models.User, user)
                
                response_body =  {
                    "content": out_message.content,
                    "timestamp": datetime.strftime(out_message.timestamp, "%d/%m/%Y at %H:%M:%S")  ,
                    "chat_id": out_message.chat_id,
                    "from_id": out_message.from_id,
                }

                response_body = json.dumps(response_body) #converts the dictionary into a json object
                header = "`".join([flag, out_message.from_id])
                response = "`".join([header,response_body])
                self.serverSocket.sendto(response.encode('utf-8'),(rec.ip_address, int(rec.server_port)))


    def login(self, sender,clientAddress):
        self.database.create_or_update(models.User, [{
            "user_id": sender,
            "ip_address": clientAddress[0], # if user is already in database, will just update IP address
            "server_port": clientAddress[1],
            "online_status": True
        }], "user_id")
        print(sender + " has logged in.")
        
    #fetches all of the chats that the user is a part of
    def chats(self, sender):
        chats = self.database.get_user_chats(sender)
        header = "`".join(["CHATS", sender])
        
        chats_str = json.dumps(chats)
        response = "`".join([header,chats_str])
        return response

    def chat(self, message_content):

        message_dict = json.loads(message_content)
        receivers = message_dict["receivers"]
        canCreate = True
        notThere = ""
        
        for receiver in receivers:
            temp = self.database.get_record_from_pk(models.User, receiver)
            #checks if all of the specified users exist in the database 
            if temp == None:
                canCreate = False
                notThere = receiver
                break

        if canCreate == True:
            print("chat created")
            print(receivers)
            self.database.get_or_create_chat(receivers)
            return (True, "")
        else:
            #WILL THIS DISPLAY SOMEWHERE??????
            # message is sent to the client if the user that they tried to create the chat with does not exist
            err = "User " + notThere + " does not exist. Chat cannot be created."
            return(False, err)

    def history(self, sender, message_content):
        message_dict = json.loads(message_content)
        chat = message_dict["chat_id"]
        header = "`".join(["HISTORY", sender])

        msgs = []

        for msg in self.database.get_chat_messages(chat_id=chat):
            msg_dict = {
                "message_id": msg.message_id,
                "content": msg.content,
                "timestamp": datetime.strftime(msg.timestamp, "%d/%m/%Y at %H:%M:%S"),
                "from_id": msg.from_id
                      }
            msgs.append(msg_dict)

        final_dict = {"chat_id": chat, "messages": msgs}
        msgs_str = json.dumps(final_dict)
        response = "`".join([header,msgs_str])
        return response

    def send(self, sender, message_content):
        print("sending message")
        message_dict = json.loads(message_content)

        msg = message_dict["message"]
        chat_id = message_dict["chat_id"]
        new_message = self.database.add_message(chat_id, msg, datetime.now(), sender)
        self.sendMessage("SEND", new_message)

    def quit(self, sender):
        self.database.create_or_update(models.User, [{
            "user_id": sender,
            "online_status": False
        }], "user_id")
        print(sender+ " has gone offline")

        header = "`".join(["QUIT",sender])
        body = dict()

        response = "`".join([header, json.dumps(body)])
        return response
       
           
    def decodeDatagram(self, datagram):

        '''
        Method to decode the datagram into the flag, sender and message content.
        
        Parameters:
            datagram: the datagram that contains the header and message content (if necessary)
        '''
        
        datagram = datagram.decode('utf-8')
        datagram_list= datagram.split("`")
        flag = datagram_list[0]
        sender = datagram_list[1]
        msg_content= datagram_list[2]
        hashed_message = datagram_list[3]
       
        return(flag, sender, msg_content, hashed_message)

    def server(self):
        
        '''
        method that listens for input from clients and responds to the messages in different ways, depending on the flags.
        '''
        print("The server is running...")
        
        while True:

            message, clientAddress = self.serverSocket.recvfrom(2048)
            print(message)
            flag, sender, message_content, hashed_message= self.decodeDatagram(message)

            server_hash =self.myHash(message_content)

            #if not(server_hash ==hashed_message):
            #    flag = "ERROR" 


            #if flag == "ERROR":
            #    self.serverSocket.sendto("ERROR".encode('utf-8'),clientAddress)
            #    print(f"server hash {server_hash }" )
            #   print(f"client hash {hashed_message}")

            #else:
            #    self.serverSocket.sendto("MATCH".encode('utf-8'),clientAddress)

            if  flag == "LOGIN": 
                self.login(sender, clientAddress)
                response = self.chats(sender)
                self.serverSocket.sendto(response.encode('utf-8'), clientAddress)        

            elif flag == "CHATS":
                response = self.chats(sender)
                self.serverSocket.sendto(response.encode('utf-8'), clientAddress)        
                
            elif flag == "CHAT":
                canCreate, response = self.chat(message_content)                
                if not(canCreate):

                    self.serverSocket.sendto(response.encode(), clientAddress)

            elif flag == "HISTORY":
                response = self.history(sender, message_content)
                self.serverSocket.sendto(response.encode('utf-8'), clientAddress)    

            elif flag == "SEND": #sends a message to a chat using the chat_id
                self.send(sender, message_content) 

            elif flag == "QUIT": #changes the user's online status to false
                response = self.quit(sender)
                self.serverSocket.sendto(response.encode('utf-8'), clientAddress)    
            
if __name__ == "__main__":
    server = Server()

            # just in case something in the refactoring is broken
'''
            if flag == "LOGIN": # add the user to the database
                database.create_or_update(models.User, [{
                    "user_id": sender,
                    "ip_address": clientAddress[0], # if user is already in database, will just update IP address
                    "server_port": clientAddress[1],
                    "online_status": True
                }], "user_id")
                print(sender + " has logged in.")

                #fetches all of the chats that the user is a part of
                chats = database.get_user_chats(sender)
                header = "`".join(["CHATS", sender])
                
                chats_str = json.dumps(chats)
                response = "`".join([header,chats_str])
                serverSocket.sendto(response.encode('utf-8'), clientAddress)
            
            elif flag == "CHATS":
                chats = database.get_user_chats(sender)
                header = "`".join(["CHATS", sender])
                
                chats_str = json.dumps(chats)
                response = "`".join([header,chats_str])
                serverSocket.sendto(response.encode('utf-8'), clientAddress)
                        elif flag == "CHAT": #creates a new chat with the specified users if one does not already exist
                message_dict = json.loads(message_content)
                receivers = message_dict["receivers"]
                canCreate = True
                notThere = ""
                
                for receiver in receivers:
                    temp = database.get_record_from_pk(models.User, receiver)
                    #checks if all of the specified users exist in the database 
                    if temp == None:
                        canCreate = False
                        notThere = receiver
                        break

                if canCreate == True:
                    print("chat created")
                    print(receivers)
                    database.get_or_create_chat(receivers)
                else:
                    #WILL THIS DISPLAY SOMEWHERE??????
                    # message is sent to the client if the user that they tried to create the chat with does not exist
                    err = "User " + notThere + " does not exist. Chat cannot be created."
                    serverSocket.sendto(err.encode(), clientAddress)
                          elif flag == "HISTORY":
                message_dict = json.loads(message_content)
                chat = message_dict["chat_id"]
                header = "`".join(["HISTORY", sender])

                msgs = []

                for msg in database.get_chat_messages(chat_id=chat):
                    msg_dict = {
                        "message_id": msg.message_id,
                        "content": msg.content,
                        "timestamp": datetime.strftime(msg.timestamp, "%d/%m/%Y at %H:%M:%S"),
                        "from_id": msg.from_id
                              }
                    msgs.append(msg_dict)

                final_dict = {"chat_id": chat, "messages": msgs}
                msgs_str = json.dumps(final_dict)
                response = "`".join([header,msgs_str])
                serverSocket.sendto(response.encode('utf-8'), clientAddress)    
                        elif flag == "SEND": #sends a message to a chat using the chat_id
                print("sending message")
                message_dict = json.loads(message_content)

                msg = message_dict["message"]
                chat_id = message_dict["chat_id"]
                new_message = database.add_message(chat_id, msg, datetime.now(), sender)
                sendMessage(flag, new_message)
                      elif flag == "QUIT": #changes the user's online status to false
                database.create_or_update(models.User, [{
                    "user_id": sender,
                    "online_status": False
                }], "user_id")
                print(sender+ " has gone offline")

                header = "`".join(["QUIT",sender])
                body = dict()

                response = "`".join([header, json.dumps(body)])
                serverSocket.sendto(response.encode('utf-8'), clientAddress)    
'''
