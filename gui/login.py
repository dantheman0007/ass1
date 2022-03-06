from tkinter import *
from tkinter import ttk
import configparser

import yaml





class LoginScreen:

    def __init__(self, root):
        root.title("Login")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.user_id = StringVar()
        id_entry = ttk.Entry(mainframe, width= 20, textvariable=self.user_id)
        id_entry.grid(column=2, row= 1, sticky=(W, E))

        ttk.Label(mainframe, text="Student Number:").grid(column=1, row = 1, sticky=W)

        ttk.Button(mainframe, text = "Log in", command=self.login).grid(column= 3, row =1, sticky = W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        id_entry.focus()
        root.bind("<Return>", self.login)



    def login(self, *args):
        uid = self.user_id.get()

        ## get verification that this person exists

        config = configparser.ConfigParser()
        config.read(".config")

        config["SESSION_INFO"]["user_id"] = uid
        config["SESSION_INFO"]["logged_in"] = "True"

        with open(".config", "w") as configfile:
            config.write(configfile)



root = Tk()

LoginScreen(root)

root.mainloop()
