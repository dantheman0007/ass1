from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from os import path

class LoginScreen(object):

    def __init__(self, parent):
        self.parent = parent

        self.root = Toplevel(parent.root)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.root.title("Login")
        self.root.geometry("550x400+300+300")

        self.create_gui()
        
    def close(self):
        self.parent.root.destroy()

    def create_gui(self):
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
        id_entry.insert(0, self.parent.user_id)

        id_entry.grid(column=2, row= 1, sticky=(W, E))

        ttk.Label(mainframe, text="Student Number:").grid(column=1, row = 1, sticky=W)


        
        self.ip_entry = ttk.Entry(mainframe, width= 20)

        self.ip_entry.insert(0, self.parent.SERVER_NAME)

        self.ip_entry.grid(column=2, row= 2, sticky=(W, E))

        ttk.Label(mainframe, text="Server IP:").grid(column=1, row = 2, sticky=W)

        ttk.Button(mainframe, text = "Log in", command=self.login).grid(column= 2, row =3, sticky = W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        id_entry.focus()
        self.root.bind("<Return>", self.login)


    def login(self, *args):
        uid = self.user_id.get()

        if self.validate_uid(uid):
            self.parent.open_home(uid, self.ip_entry.get())
            self.root.destroy()
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
