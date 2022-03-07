from tkinter import *
from tkinter import ttk
import configparser
from functools import partial
import placeholder


class HomeScreen(object):

        chats = []

        user_id = None

        def __init__(self, parent) -> None:

            self.ph = placeholder.Placeholder()

            self.parent = parent
            self.root = Toplevel(parent.root)

            self.load_config()
            self.load_chats()
            
            self.root.title("Home")
            self.root.geometry("550x400+300+300")
            

            self.draw_gui()
            
            pass


        def draw_gui(self):
            self.mainframe = ttk.Frame(self.root, padding = 10)
            self.mainframe.grid(column=0, row=0)
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
            self.draw_gui()


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