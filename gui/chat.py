
from tkinter import *
from tkinter import ttk
import configparser

from functools import partial


import placeholder
import json


class ChatScreen:

    chats = []

    user_id = None


    def __init__(self, root, chat_id) -> None:

        self.ph = placeholder.Placeholder()
        self.chat_id = chat_id


        self.load_config()
        self.load_chat_data()


        root.title("Chat")

        mainframe = ttk.Frame(root, padding = 10)
        mainframe.grid(column=0, row=0)


        message_frame = ttk.Frame(mainframe, padding = 10)
        message_frame.grid(row=1, column=0, columnspan=2)


        self.message_box = ttk.Text()

        messages = []

        ttk.Label(mainframe, text = "Chats for {}".format(self.user_name)).grid(row=0, column = 0)

        for i, chat in enumerate(self.chats):

            # #f = ttk.Frame(chats_frame, relief="solid", borderwidth=5, width=200, height= 100, padding=10)
            # f.grid(row = i+1, column =4, columnspan=4, sticky=(E, W) ,pady=5)
            

            # ttk.Label(f, text = chat["chat_name"]).grid(row = i, column =0,sticky=W)

            # f.bind("<Button-1>", partial(self.go_to_chat, chat["chat_id"]))

            # frames.append(f)

            pass

        pass

    def load_chat_data(self):
        with open("chats/{}.json".format(self.chat_id), "r") as read_file:
            self.messages = json.load(read_file)
            print(self.messages)


    def load_config(self):
        config = configparser.ConfigParser()
        config.read(".config")

        self.user_id = config["SESSION_INFO"]["user_id"]
        self.user_name = config["SESSION_INFO"]["user_name"]

    def load_chats(self):
        self.chats = self.ph.ph_get_chats(self.user_id)

    def go_to_chat(self, chat_id, btn_press):
        self.ph.get_messages(chat_id)
        print(chat_id)



root = Tk()

ChatScreen(root, "167831c0-be28-4689-b040-49048118956e")

root.mainloop()