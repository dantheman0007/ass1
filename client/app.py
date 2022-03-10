from tkinter import *
from os import path
from functools import partial
from datetime import datetime
import client
import configparser
import login, home, chat

class ChatApp(object):

    chats = list()
    chat_screens = dict()
    
    SERVER_NAME = "196.47.216.151"
    SERVER_PORT = 9999
    
    def __init__(self) -> None:        
        self.load_config()
        self.root = Tk()

        self.loginScreen = login.LoginScreen(self)

        self.root.withdraw()
        self.root.mainloop()


        pass

    def open_home(self, user_id, server_ip):

        config = configparser.ConfigParser()
        config.read(".config")

        config["SESSION_INFO"]["server_ip"] = server_ip
        config["SESSION_INFO"]["user_id"] = user_id

        with open(".config", "w") as configfile:
            config.write(configfile)


        self.user_id = user_id
        self.SERVER_NAME = server_ip
        
        self.client = client.Client(self)
        self.hs= home.HomeScreen(self)
        self.hs.redraw_chat_frame()

    def fetch_messages(self, chat_id, *args):
        self.client.get_messages(chat_id)
        
        

    def open_chat_screen(self, chats):
        self.chat_screens[chats["chat_id"]] = {
            "chat_screen": chat.ChatScreen(self, chats),
            "open": True
        }

    def start_new_chat(self, user_ids):
        print(user_ids)

    def load_chats(self):
            #self.chats = self.ph.ph_get_chats(self.user_id)
        pass

    def load_config(self):

        if not path.exists(".config"):
            config = configparser.ConfigParser()

            config["SESSION_INFO"] = {
                "server_ip": "",
                "user_id": ""
            }

            with open(".config", "w") as configfile:
                config.write(configfile)

        
        config = configparser.ConfigParser()
        config.read(".config")

        self.SERVER_NAME = config["SESSION_INFO"]["server_ip"]
        self.user_id = config["SESSION_INFO"]["user_id"]



if __name__ == "__main__":
    ChatApp()