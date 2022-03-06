# SERVER

import socket
import threading
import models
import db
import uuid

serverPort = 9999 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initialising server object
serverSocket.bind(("",serverPort)) # bind to local host

# these will need to be replaced by the database
senders= [] # e.g [client1, client2]
receivers=[]    # [client2, client1]        if client1 talking to client 2 and vice versa
addresses= []   # [add_client1, add_client2]
INITIAL_CONNECTION="You are connected"
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
def sendMessage(message, receiver): # message should already be encoded
    
    # TODO make loop to go over everyone in list from db
    
    rec = database.get_record_from_pk(models.User, receiver)

    if rec == None:
        print("User does not exist. Message stored in database.")

    else:
        serverSocket.sendto(message.encode(),(rec.ip_address, int(rec.server_port)))
    
    '''
    if message== INITIAL_CONNECTION:    # for the intial connection between two clients, show that connection was successful
        serverSocket.sendto(message.encode('utf-8'),addresses[receivers.index(receiver)])   # find address at index of receiver (this will change with database)

        
    elif receiver in senders:   # check if the receiver of message has logged in
        #send message to recipientClient
        index = senders.index(receiver)
        print(f"receiver {receiver} index: {index}")
        serverSocket.sendto(message.encode('utf-8'),addresses[index])

    else:
        print("receiver not in list")
        serverSocket.sendto("User not in list.".encode('utf-8'),addresses[receivers.index(receiver)])'''

        
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
        #return(sender, receiver, f"{sender} has disconnected.")
    
def main():
    
    print("The server is running...")
    while True:

        message, clientAddress = serverSocket.recvfrom(2048)
        
        flag, id, receiver, msg= decodeHeader(message)
        print(flag)
        #print(receiver)
        #print((database.get_record_from_pk(models.User, receiver)).user_id)

        if flag == "LOGIN": # add the user to the database
            database.create_or_update(models.User, [{
                "user_id": id,
                "ip_address": clientAddress[0], # if user is already in database, will just update IP address
                "server_port": clientAddress[1]
            }], "user_id")
            loginConfirm = "Login successful."
            serverSocket.sendto(loginConfirm.encode(), clientAddress)

        elif flag == "CHAT": 
            receivers = receiver.split(" ") #list of receivers, one for normal chat, multiple for group
            print(receivers)
            chatID = str(uuid.uuid4())
            database.create_or_update(models.Chat,[{
                "chat_id": chatID,
                "chat_name": id + " " + receiver
                }], "chat_id")

        elif flag == "SEND":
            print("sending message")
            sendMessage(msg, receiver)

        # modifiedMessage = message.decode('utf-8').upper() # decode from bytes
        # serverSocket.sendto(modifiedMessage.encode('utf-8'),clientAddress)
        
if __name__ == "__main__":
    main()
