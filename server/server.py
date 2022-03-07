# SERVER

import socket
import threading
import models
import db
import sqlalchemy
from datetime import datetime

serverPort = 9999 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initialising server object
serverSocket.bind(("",serverPort)) # bind to local host
database = db.DB()


def myHash(text:str):
  hash=0
  for ch in text:
    hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
  return hash

# takes in the message from sender and sends to receiver
def sendMessage(senderID, receiver, message): # message should already be encoded
    
    # TODO make loop to go over everyone in list from db
    
    rec = database.get_record_from_pk(models.User, receiver)

    if rec == None:
        sender = database.get_record_from_pk(models.User, senderID)
        message = "User " + receiver + " does not exist."
        serverSocket.sendto(message.encode(),(sender.ip_address, int(sender.server_port)))

    elif rec.online_status == False:
        sender = database.get_record_from_pk(models.User, senderID)
        message = "User " + receiver + " is offline. Message has been stored."
        serverSocket.sendto(message.encode(),(sender.ip_address, int(sender.server_port)))
    
    else:
        serverSocket.sendto(message.encode(),(rec.ip_address, int(rec.server_port)))

        
# this will be used to decode headers
# TODO implement protocol into here
def decodeDatagram(datagram):

    datagram = datagram.decode('utf-8')
    datagram_list= datagram.split("`")
    flag = datagram_list[0]
    sender = datagram_list[1]
    msg_content= datagram_list[2]

    return(flag, sender, msg_content)
    '''
    if flag == "LOGIN":
        return (flag, sender, "", "") 
    elif flag == "SEND":
        receiver= dgram[9:18]
        senderMessage= dgram[18:]
        return (flag, sender, receiver, senderMessage)
    elif flag == "CHAT":
        receiver = dgram[9:] #list of users (can be one) to chat with, separated by spaces
        return (flag, sender, receiver, "")
    elif flag == "QUIT":
        return(flag, sender, "", "")
    '''


def main():
    
    print("The server is running...")
    while True:

        message, clientAddress = serverSocket.recvfrom(2048)
        
        flag, from, message_content= decodeDatagram(message)

        if flag == "LOGIN": # add the user to the database
            database.create_or_update(models.User, [{
                "user_id": id,
                "ip_address": clientAddress[0], # if user is already in database, will just update IP address
                "server_port": clientAddress[1],
                "online_status": True
            }], "user_id")
            print(id + " has logged in.")
            loginConfirm = "Login successful."
            serverSocket.sendto(loginConfirm.encode(), clientAddress)

            #print out all of the chats that the user is a part of
            chats = database.get_user_chats(id)
            allChats = "Available chats: \n"

            for x in chats:
                temp = x.get("chat_id")
                if x != chats[-1]:
                    allChats = allChats + temp + " \n"
                else:
                    allChats = allChats + temp
                

            serverSocket.sendto(allChats.encode(), clientAddress)


        elif flag == "CHAT": 
            receiver = id + " " + receiver
            receivers = receiver.split(" ") #list of receivers, one for normal chat, multiple for group
            canCreate = True
            notThere = ""
            for receiver in receivers:
                temp = database.get_record_from_pk(models.User, receiver)
                if temp == None:
                    canCreate = False
                    notThere = receiver
                    break

            if canCreate == True:
                database.get_or_create_chat(receivers)
            else:
                err = "User " + notThere + " does not exist. Chat cannot be created."
                serverSocket.sendto(err.encode(), clientAddress)


            try:
                database.get_or_create_chat(receivers)
            except sqlalchemy.orm.exc.FlushError:
                print("User does not exist in the database.")

        elif flag == "SEND":
            print("sending message")
            #add message to the database
            database.add_message(chat_id, msg, datetime.now(), id)
            #need to map the recipients to the chat_id
            sendMessage(id, receiver, msg)

        elif flag == "QUIT":
            database.create_or_update(models.User, [{
                "user_id": id,
                "online_status": False
            }], "user_id")
            print(id + " has gone offline")


        # modifiedMessage = message.decode('utf-8').upper() # decode from bytes
        # serverSocket.sendto(modifiedMessage.encode('utf-8'),clientAddress)
        
if __name__ == "__main__":
    main()
