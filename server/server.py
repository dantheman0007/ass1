# SERVER

import socket
import threading

serverPort = 9999 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initialising server object
serverSocket.bind(("",serverPort)) # bind to local host

# these will need to be replaced by the database
senders= [] # e.g [client1, client2]
receivers=[]    # [client2, client1]        if client1 talking to client 2 and vice versa
addresses= []   # [add_client1, add_client2]
INITIAL_CONNECTION="You are connected"

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
    
    if message== INITIAL_CONNECTION:    # for the intial connection between two clients, show that connection was successful
        serverSocket.sendto(message.encode('utf-8'),addresses[receivers.index(receiver)])   # find address at index of receiver (this will change with database)
        
    elif receiver in senders:   # check if the receiver of message has logged in
        #send message to recipientClient
        index = senders.index(receiver)
        print(f"receiver {receiver} index: {index}")
        serverSocket.sendto(message.encode('utf-8'),addresses[index])

    else:
        print("receiver not in list")
        serverSocket.sendto("User not in list.".encode('utf-8'),addresses[receivers.index(receiver)])

        
# this will be used to decode headers, currently only decodes the sender and receiver
# TODO implement protocol into here
def decodeHeader(datagram):

    dgram= datagram.decode('utf-8')
    sender= dgram[0:9]
    receiver= dgram[9:18]

    if len(dgram)<=18: # if the datagram doesnt contain message (only client usernames)
        print(f"initial connection: {sender}")
        return(sender, receiver, "You are connected")
    
    else: # len(dgram)> 18: i.e. the datagram contains a message and isnt just the initial connection
        senderMessage= dgram[18:]
        if senderMessage== "QUIT":
            return(sender, receiver, f"{sender} has disconnected.")
        return(sender, receiver, senderMessage)
    
def main():
    
    print("The server is running...")
    while True:

        message, clientAddress = serverSocket.recvfrom(2048)
        
        sender, receiver, msg= decodeHeader(message)

        if msg == INITIAL_CONNECTION: # add to the list of user
            senders.append(sender)
            addresses.append(clientAddress)
            receivers.append(receiver)
            print(f"current list of senders: {senders}") 
            print(f"current list of receivers: {receivers}") 
        
        sendMessage(msg, receiver)

        # modifiedMessage = message.decode('utf-8').upper() # decode from bytes
        # serverSocket.sendto(modifiedMessage.encode('utf-8'),clientAddress)
        
if __name__ == "__main__":
    main()
