# SERVER

import socket
import threading

serverPort = 9999 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # initialising server object
serverSocket.bind(("",serverPort)) # bind to local host


senders= []
receivers=[]
addresses= []
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
def sendMessage(message, receiver): # message should already be encoded
    
    # make loop to go over everyone in list from db
    if message== INITIAL_CONNECTION:
        serverSocket.sendto(message.encode('utf-8'),addresses[receivers.index(receiver)]) # send message to clients address?

    elif receiver in senders:
        #send message to recipientClient
        index = senders.index(receiver)
        print(f"receiver {receiver} index: {index}")
        serverSocket.sendto(message.encode('utf-8'),addresses[index]) # send message to clients address?

    else:
        print("receiver not in list")
        # send message to sendClient that could not find recipientClient

def decodeHeader(message):
    msg = message.decode('utf-8')
    sender= msg[0:9]
    receiver= msg[9:18]

    if len(msg)<=18:
        print(f"initial connection: {sender}")
        return(sender, receiver, "You are connected")
    
    else: # len(msg)> 18: i.e. the datagram contains a message and isnt just the initial connection
        senderMessage= msg[18:]
        if senderMessage== "QUIT":
            return(sender, receiver, f"{sender} has disconnected.")
        return(sender, receiver, senderMessage)
    
def main():
    
    print("The server is running...")
    while True:

        message, clientAddress = serverSocket.recvfrom(2048)
        
        sender, receiver, msg= decodeHeader(message)

        if msg == INITIAL_CONNECTION:
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
