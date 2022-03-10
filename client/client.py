import socket
import threading
import json
from tkinter import *

# print (u'\u2713') TICK SYMBOL
class Client:
    """
    Client class that handles communication between the server and the GUI
    """

    def __init__(self, parent) -> None:
        """
        Initialises the clients socket and class boolean variables
        Starts a thread to listen for incoming messages

        Parameters:
            parent: parent class, for GUI communication
        """
        self.parent = parent
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._is_running= True
        self.waiting_for_ack= True 
        self.ack= True
        host_name = socket.gethostname()
        client_ip = socket.gethostbyname(host_name)

        self.login()

        listenMessage = threading.Thread(target=self.listenForMessage, )
        listenMessage.start()
        
    def stop(self):
        """
        Called by gui to end the program
        """
        self._is_running = False

    def create_request(self, flag, **kwargs):
        """
        takes in a protocol flag and creates a request for server
        request format: FLAG`SENDER`MESSAGE_PAYLOAD

        Parameters:
            flag: keyword that informs server what process to carry out 
        """
        header = "`".join([flag, self.parent.user_id])
        
        payload = {}

        for key, value in kwargs.items():
            payload[key] = value

        payload_str = json.dumps(payload)
        hash_payload = self.myHash(payload_str)
        request = "`".join([header, payload_str,hash_payload])
        return request

    def send_request(self, request):
        """
        Sends request to server

        Parameters:
            request: datagram to be sent to server, in format that follows protocol
        """
        print("Sending: "+request)
        self.client_socket.sendto(request.encode("utf-8"), (self.parent.SERVER_NAME, self.parent.SERVER_PORT))
        
        

    def send_message(self, message, chat_id):
        """
        Sends users message to server
        Waits for ACK from server before advancing

        Parameters:
            message: outgoing message to server -> client_ip
            chat_id: unique ID associated with a chat
        """
        request = self.create_request("SEND", message = message, chat_id = chat_id)

        self.client_socket.sendto(request.encode("utf-8"), (self.parent.SERVER_NAME, self.parent.SERVER_PORT))
        print("Sending message: " + request)
        self.waiting_for_ack= True

        while(self.waiting_for_ack):
            continue
            # wait for server to return an ACK

        if not(self.ack):
            self.send_message(message, chat_id)
            # if server returns NACK, resend message

        # server received correct message
        pass 

    def login(self):
        """
        creates login request for server
        """
        request = self.create_request("LOGIN")
        self.send_request(request)

    def new_chat(self, users):
        """
        creates new chat request for server
        updates GUI with new chats

        Parameters:
            users: list of all users needed for new chat
        """
        print("Making new chat with: ", users)
        request = self.create_request("CHAT", receivers = users)
        self.send_request(request)
        self.parent.hs.draw_gui()
        pass

    def refresh_chats(self):
        """
        retreives latest version of users chats from database
        """
        request = self.create_request("CHATS")
        self.send_request(request)
        pass

    def log_out(self):
        """
        informs server that user is Logging
        ends the thread listening for incoming messages
        """
        print("Logging off.") 
        request = self.create_request("QUIT")
        self.send_request(request)
        self.stop()

    def get_messages(self, chat_id):
        """
        retrieve all chats and chat history from server

        Parameters:
            chat_id: unique ID associated with a chat
        """
        request = self.create_request("HISTORY", chat_id = chat_id)
        self.send_request(request)

    def listenForMessage(self):
        """
        Runs in own thread
        Listens for incoming messages
        """
        while (self._is_running):
            receivedMessage, serverAddress = self.client_socket.recvfrom(1000000)
            print("listenForMessage "+receivedMessage.decode())
            self.decode_message(receivedMessage.decode())
            
        return
            
    def decode_message(self, response):
        """
        decodes the incoming messages from server based on flags/headers 
        follows our datagram protocol

        Parameters:
            response: datagram received from server
        """ 
        response = response.split("`")
        flag = response[0]
        sender = response[1]
        msg_content= response[2]

        if flag =="ACK":
            payload = json.loads(msg_content)
            message = payload["message"]
            
            if message== "online":
                self.ack= True
                # tell chat.py that user is online, 
                # chat.py has online var and online_status()
                # should print 2 ticks under message
                # user online
            elif message=="offline":
                self.ack=True
                # user offline
                # tell chat.py that user is offline, 
                # chat.py has online var and online_status()
                # should print 1 ticks under message

            else:
                self.ack = False
                print(message)
                print("server received wrong message...resending")

            self.waiting_for_ack = False 
            
        elif flag == "CHATS":
            self.parent.chats = json.loads(msg_content)
            print("Parent chats:",  self.parent.chats)
            self.parent.hs.draw_gui()

        elif flag == "CHAT":
            payload = json.loads(msg_content)
            err = payload["error"]
            
            if err != "":
                self.parent.hs.error_window(err)

        elif flag == "SEND":
            payload = json.loads(msg_content)
            if payload["chat_id"] in self.parent.chat_screens:
                self.parent.chat_screens[payload["chat_id"]].write_message(payload)
            else:
                print("New message received from {}".format(payload["from_id"]))
        
        elif flag == "HISTORY":
            payload = json.loads(msg_content)

            self.parent.open_chat_screen(payload)

        elif flag == "QUIT":
            self.stop()

        pass

    
    def myHash(self, text):
        """
        simple hash function to hash the message of our datagram
        used by server to ensure correct message was received

        Parameters:
            text: str needing to be hashed

        Returns hash value associated with the text
        """
        hash=0
        for ch in text:
            hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
        return str(hash)
