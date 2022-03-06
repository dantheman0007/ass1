
from tkinter import *
from tkinter import ttk
import configparser
from functools import partial
import placeholder
import chat

class HomeScreen:

    chats = []

    user_id = None

    def __init__(self, root) -> None:

        self.ph = placeholder.Placeholder()

        self.load_config()
        self.load_chats()


        root.title("Home")

        mainframe = ttk.Frame(root, padding = 10)
        mainframe.grid(column=0, row=0)


        chats_frame = ttk.Frame(mainframe, padding = 10)
        chats_frame.grid(row=1, column=0, padx=200)

        frames = []

        ttk.Label(mainframe, text = "Chats for {}".format(self.user_id)).grid(row=0, column = 0)

        for i, chat in enumerate(self.chats):

            f = ttk.Frame(chats_frame, relief="solid", borderwidth=5, width=200, height= 100, padding=10)
            f.grid(row = i+1, column =4, columnspan=4, sticky=(E, W) ,pady=5)
            

            l = ttk.Label(f, text = chat["chat_name"])
            l.grid(row = i, column =0,sticky=W)

            f.bind("<Button-1>", partial(self.open_chat, chat["chat_id"]))
            l.bind("<Button-1>", partial(self.open_chat, chat["chat_id"]))

            frames.append(f)

            pass

        pass

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(".config")

        self.user_id = config["SESSION_INFO"]["user_id"]

    def load_chats(self):
        self.chats = self.ph.ph_get_chats(self.user_id)

    def open_chat(self, chat_id, btn_press):
        self.ph.get_messages(chat_id)
        print(chat_id)

        chat.new_chat_window(chat_id)




def open_window():

    root = Tk()

    HomeScreen(root)

    root.mainloop()