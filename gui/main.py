from logging import PlaceHolder
from tkinter import *
from tkinter import ttk
import configparser

from numpy import place
from sqlalchemy import column
import placeholder


class HomeScreen:

    chats = []

    user_id = None


    def __init__(self, root) -> None:

        self.ph = placeholder.Placeholder()

        self.load_config()
        self.load_chats()


        root.title("Home")

        root.geometry("600x500")

        mainframe = ttk.Frame(root)
        mainframe.grid(column=0, row=0)

        frames = []

        for i, chat in enumerate(self.chats):

            f = ttk.Frame(mainframe, relief="solid", borderwidth=5, width=200, height= 100)
            f.grid(row = i, column =4, columnspan=4)
            

            ttk.Label(f, text = chat["chat_id"]).grid(row = i, column =0,sticky=W)

            frames.append(f)

            pass


        # for child in mainframe.winfo_children(): 
        #     child.grid_configure(padx=5, pady=5)

        pass

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(".config")

        self.user_id = config["SESSION_INFO"]["user_id"]

    def load_chats(self):
        self.chats = self.ph.ph_get_chats(self.user_id)



root = Tk()

HomeScreen(root)

root.mainloop()