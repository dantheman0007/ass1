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
        self._is_running = False

    def create_request(self, flag, **kwargs):
        header = "`".join([flag, self.parent.user_id])
        
        payload = {}

        for key, value in kwargs.items():
            payload[key] = value

        payload_str = json.dumps(payload)
        hash_payload = self.myHash(payload_str)
        request = "`".join([header, payload_str,hash_payload])
        return request

    def send_request(self, request):
        print("Sending: "+request)
        self.client_socket.sendto(request.encode("utf-8"), (self.parent.SERVER_NAME, self.parent.SERVER_PORT))
        
        #receivedMessage, serverAddress = self.client_socket.recvfrom(1000000)
        #if receivedMessage.decode('utf-8')=="ERROR":
        #    print("server received wrong message...resending")
        #    self.send_request(request)
        #else: print("no error")
        

    def send_message(self, message, chat_id):
        request = self.create_request("SEND", message = message, chat_id = chat_id)

        self.client_socket.sendto(request.encode("utf-8"), (self.parent.SERVER_NAME, self.parent.SERVER_PORT))
        print("Sending message: " + request)
        self.waiting_for_ack= True

        while(self.waiting_for_ack):
            continue

        if not(self.ack):
            self.send_message(message, chat_id)

        else:
            print(u'\u2713')
        
        #self.send_request(request)

    def login(self):
        request = self.create_request("LOGIN")
        self.send_request(request)

    def new_chat(self, users):
        print("Making new chat with: ", users)
        request = self.create_request("CHAT", receivers = users)
        self.send_request(request)
        self.parent.hs.draw_gui()
        pass

    def refresh_chats(self):
        request = self.create_request("CHATS")
        self.send_request(request)
        pass

    def log_out(self):
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
            print("listenForMessage "+receivedMessage.decode())
            self.decode_message(receivedMessage.decode())
            
        return
            
            
    def decode_message(self, response):
        
        print("Reponse"+response)
        response = response.split("`")
        flag = response[0]
        sender = response[1]
        msg_content= response[2]

        if flag =="ACK":
            payload = json.loads(msg_content)
            err = payload["error"]
            
            if err == "":
                self.ack= True
            else:
                self.ack = False
                print(err)
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
            #print(err)

        elif flag == "SEND":
            payload = json.loads(msg_content)
            self.parent.chat_screens[payload["chat_id"]].write_message(payload)
        
        elif flag == "HISTORY":
            payload = json.loads(msg_content)

            self.parent.open_chat_screen(payload)

        elif flag == "QUIT":
            self.stop()

        pass

    
    def myHash(self, text):
        hash=0
        for ch in text:
            hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
        return str(hash)
