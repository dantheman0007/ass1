# SERVER

import socket
import threading
import models
import db

serverPort = 9999 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initialising server object
serverSocket.bind(("",serverPort)) # bind to local host
database = db.DB()


'''
def handleConnection(client): # not sure what client passing, function: get client from accept method and pass to handle connection
    stop= False
    while not stop:
        try:
            message= client.recvfrom(2048) # try get message from client
            print(client)
            sendMessage(message) # If get message, send it

        except:
            # handle if client no longer has connection 
            # remove them from list 
            # send message to recipientClient (sender left)
            stop = True 
'''

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

        
# this will be used to decode headers, currently only decodes the sender and receiver
# TODO implement protocol into here
def decodeHeader(datagram):

    datagram = datagram.decode('utf-8')
    info = datagram.split("`")
    flag = info[0]
    dgram = info[1]
    sender= dgram[0:9]

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
    
def main():
    
    print("The server is running...")
    while True:

        message, clientAddress = serverSocket.recvfrom(2048)
        
        flag, id, receiver, msg= decodeHeader(message)

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

        elif flag == "CHAT": 
            receivers = receiver.split(" ") #list of receivers, one for normal chat, multiple for group
            print(receivers)
            chatID = ''
            database.create_or_update(models.Chat,[{
                "chat_id": chatID,
                "chat_name": id + " " + receiver
                }], "chat_id")

        elif flag == "SEND":
            print("sending message")
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
