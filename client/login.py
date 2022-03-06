from email import message
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import configparser
import tkinter

from sqlalchemy import false
import main as hs

class LoginScreen:

    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

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
            
            self.root.destroy()

            hs.open_window()
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


if __name__ == "__main__":
    root = Tk()
    LoginScreen(root)
    root.mainloop()