from tkinter import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import configparser
import main as hs
from os import path
import placeholder
import json
from functools import partial
from datetime import datetime
import client

class ChatApp(object):

    def __init__(self) -> None:

        self.chat_screens = dict()

        self.client = client.Client(self)
        
        self.root = Tk()
        self.loginScreen = self.LoginScreen(self)

        self.root.mainloop()
        self.chat_screens = {}
        self.ChatScreen(self, "e6070836-3b69-4da1-b6ef-7dfabcda5d14")
        
        pass

    def open_home(self):
        self.hs= self.HomeScreen(self)

    def open_chat_screen(self, chat_id):
        self.chat_screens[chat_id] = self.ChatScreen(self, chat_id)


    class LoginScreen(object):

        def __init__(self, parent):
            self.parent = parent
            self.root = parent.root


            self.root.title("Login")
            self.root.geometry("550x400+300+300")

            self.root.grid_rowconfigure(0, weight = 1)
            self.root.grid_columnconfigure(0, weight = 1)
            # win = Tk()
            # win.geometry("500x500")
            mainframe = ttk.Frame(self.root, padding="3 3 12 12")
            mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
            
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            
            # mainframe.pack()
            self.user_id = StringVar()
            id_entry = ttk.Entry(mainframe, width= 20, textvariable=self.user_id)

            ## Used for testing purposes
            id_entry.insert(0, "LJNDAN001")

            id_entry.grid(column=2, row= 1, sticky=(W, E))

            ttk.Label(mainframe, text="Student Number:").grid(column=1, row = 1, sticky=W)

            ttk.Button(mainframe, text = "Log in", command=self.login).grid(column= 3, row =1, sticky = W)

            for child in mainframe.winfo_children(): 
                child.grid_configure(padx=5, pady=5)

            id_entry.focus()
            self.root.bind("<Return>", self.login)

        def login(self, *args):
            uid = self.user_id.get()

            if self.validate_uid(uid):
                config = configparser.ConfigParser()
                config.read(".config")

                config["SESSION_INFO"]["user_id"] = uid

                with open(".config", "w") as configfile:
                    config.write(configfile)
                

                self.parent.open_home()
            else:
                messagebox.showerror(self.root, "Please enter a valid student number")


        def has_numbers(self, input):
            return any(char.isdigit() for char in input)

        def has_letters(self, input):
            return any(c.isalpha() for c in input)

        def validate_uid(self, uid):

            if len(uid) != 9:
                return False
            else:
                str_part = uid[0:6]
                int_part = uid[6:9]

                if self.has_letters(int_part) or self.has_numbers(str_part):
                    return False
            
            return True


    class HomeScreen(object):

        chats = []

        user_id = None

        def __init__(self, parent) -> None:

            self.ph = placeholder.Placeholder()

            self.load_config()
            self.load_chats()
            self.parent = parent
            self.root = Toplevel(parent.root)
            self.root.title("Home")
            self.root.geometry("550x400+300+300")
            self.mainframe = ttk.Frame(self.root, padding = 10)
            self.mainframe.grid(column=0, row=0)

            self.draw_chat_frame()
            
            pass

        def draw_chat_frame(self):
            self.chats_frame = ttk.Frame(self.mainframe, padding = 10)
            self.chats_frame.grid(row=2, column=0, padx=200)

            frames = []

            ttk.Label(self.mainframe, text = "Chats for {}".format(self.user_id)).grid(row=1, column = 0)

            btn_new_chat = ttk.Button(self.chats_frame, text = "New Chat", command = self.new_chat_window)

            btn_new_chat.grid(row = 0, column= 4)

            for i, chat in enumerate(self.chats):

                f = ttk.Frame(self.chats_frame, relief="solid", borderwidth=5, width=200, height= 100, padding=10)
                f.grid(row = i+1, column =4, columnspan=4, sticky=(E, W) ,pady=5)
                

                l = ttk.Label(f, text = chat["chat_name"])
                l.grid(row = i, column =0,sticky=W)

                f.bind("<Button-1>", partial(self.open_chat, chat["chat_id"]))
                l.bind("<Button-1>", partial(self.open_chat, chat["chat_id"]))
    
                frames.append(f)

                pass


        def new_chat_window(self, *args):
            top= Toplevel(self.root)
            top.geometry("350x150")

            lbl = ttk.Label(top, text="Enter the list of users you want to talk to, separated by a space:", wraplength=150)
            lbl.pack(pady=5 )
            entry= Entry(top, width= 50)
            entry.pack()
            entry.bind("<Return>",  lambda x:self.close_win(top, entry))
            button= Button(top, text="Ok", command=lambda:self.close_win(top, entry))
            button.pack(pady=5, side= TOP)

            entry.focus()

        def close_win(self, top, entry):
            
            users = entry.get().split()
            users.append(self.user_id)
            print(users)
            top.destroy()
            self.redraw_chat_frame()
            

        def redraw_chat_frame(self):
            self.load_chats()
            self.chats_frame.grid_forget()
            self.draw_chat_frame()

        def load_config(self):
            config = configparser.ConfigParser()
            config.read(".config")

            self.user_id = config["SESSION_INFO"]["user_id"]

        def load_chats(self):
            self.chats = self.ph.ph_get_chats(self.user_id)

        def open_chat(self, chat_id, btn_press):
            self.ph.get_messages(chat_id)
            print(chat_id)
            self.parent.open_chat_screen(chat_id)

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
            self.write_messages()
            
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
                "msg_content": self.message_compose.get(),
                "timestamp": datetime.strftime(datetime.now(), "%d/%m/%Y at %H:%M:%S"),
                "from_id": self.user_id
            }
            
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
                message_dict["msg_content"]+"\n\n", (justify_right, "regular_text",))


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



if __name__ == "__main__":
    ChatApp()