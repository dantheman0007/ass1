from tkinter import *
from tkinter import ttk
import configparser
from functools import partial
from datetime import datetime

import placeholder
import json


class ChatScreen:

        chats = []

        user_id = None


        def __init__(self, parent, chat_id) -> None:
            self.parent = parent
            self.root = Toplevel(parent.root)
            self.root.geometry("580x550+850+300")
            self.ph = placeholder.Placeholder()
            self.chat_id = chat_id

            self.load_config()
            
            self.load_chat_data()


            self.root.title("Chat")

            
            self.setup_gui()
            pass


        def setup_gui(self):

            # Main Frame
            mainframe = ttk.Frame(self.root, padding = 10)
            mainframe.grid(column=0, row=0)

            #Message Frame
            message_frame = ttk.Frame(mainframe, padding = 10)
            message_frame.grid(row=1, column=0, columnspan=2)

            #Message Box (where messages are written to)
            self.message_box = Text(message_frame, width = 50, height = 25)
            self.message_box.grid(row = 1, column=0, columnspan = 2)
            
            # Message box tags for formatting text
            self.message_box.tag_configure("bold", font=("Calibri", 10, "bold"))
            self.message_box.tag_configure("muted", font=("Calibri", 10), foreground="grey")
            self.message_box.tag_configure("just_right", font=("Calibri", 10), justify="right")
            self.message_box.tag_configure("bold_just_right", font=("Calibri", 10, "bold"), justify="right")
            self.message_box.tag_configure("regular_text", font=("Calibri", 10))
            
            # Writes the message history to the chat box
            # self.write_messages()
            
            # New message input
            self.new_message = StringVar()
            self.message_compose = ttk.Entry(message_frame, textvariable=self.new_message, width=50)
            self.message_compose.grid(column=0, row = 2, pady=10)
            self.message_compose.focus()
            self.message_compose.bind("<Return>", self.send_message)

            # Send button
            send_button = ttk.Button(message_frame, command=self.send_message, text="Send")
            send_button.grid(column=1, row = 2)

            ttk.Label(mainframe, text = "Chats for {}".format(self.user_id)).grid(row=0, column = 0)


        def send_message(self, *args):
            out_dict = {
                "content": self.message_compose.get(),
                "timestamp": datetime.strftime(datetime.now(), "%d/%m/%Y at %H:%M:%S"),
                "from_id": self.user_id
            }
            
            self.parent.client.send_message(self.message_compose.get(), self.chat_id)

            
            self.message_compose.delete(first = 0, last= len(self.message_compose.get()))

            
            self.write_message(out_dict)
            pass


        def write_message(self, message_dict):
            if self.user_id == message_dict["from_id"]:
                justify_right = "just_right"
            else:
                justify_right = ""
                
            self.message_box.insert("end", 
                message_dict["from_id"],
                ("bold", justify_right))

            self.message_box.insert("end", 
                " - "+message_dict["timestamp"]+"\n",
                ("muted", justify_right))

            self.message_box.insert("end", 
                message_dict["content"]+"\n\n", (justify_right, "regular_text",))


        def write_messages(self):

            for i, message in enumerate(self.chat_data["messages"]):

                self.write_message(message)


        def load_chat_data(self):
            with open("chats/{}.json".format(self.chat_id), "r") as read_file:
                self.chat_data = json.load(read_file)

            self.participants = self.chat_data["chat_participants"]


        def load_config(self):
            config = configparser.ConfigParser()
            config.read(".config")

            self.user_id = config["SESSION_INFO"]["user_id"]
