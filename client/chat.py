from tkinter import *
from tkinter import ttk
from datetime import datetime


class ChatScreen:
    """
    GUI for an individual chat, where users can input text and send it to the specified chat

    Properties:
        messages (list): a list of all the chat history for this particular chat
    """
    messages = []

    def __init__(self, parent, chats) -> None:
        self.parent = parent
        self.root = Toplevel(parent.root)
        self.root.geometry("580x550+850+300")
        self.root.protocol("WM_DELETE_WINDOW", self.close_chat_window)
        self.online=False 
        self.chat_id = chats["chat_id"]
        self.messages = chats["messages"]
        
        self.participants = self.chat_id.split("-")
        self.participants.remove(self.parent.user_id)
        
        if len(self.participants) > 1:
                self.participants = " - ".join(self.participants)

        self.root.title("Chat")

        
        self.setup_gui()
        pass


    def setup_gui(self):
        """
        Creates the GUI for that chat screen
        """

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

        ttk.Label(mainframe, text = "Chat with {}".format(self.participants)).grid(row=0, column = 0)


    def send_message(self, *args):
        """
        Handles all aspects of sending a message, including writing it to the screen and sending it to the server.
        """

        out_dict = {
            "content": self.message_compose.get(),
            "timestamp": datetime.strftime(datetime.now(), "%d/%m/%Y at %H:%M:%S"),
            "from_id": self.parent.user_id
        }
        
        self.parent.client.send_message(self.message_compose.get(), self.chat_id)
        
        
        self.message_compose.delete(first = 0, last= len(self.message_compose.get()))
        self.write_message(out_dict)
        pass


    def close_chat_window(self):
        """
        Called when closing the chat screen. Takes care of removing this chat instance from the list of open chat screens
        """
        del self.parent.chat_screens[self.chat_id]
        self.root.destroy()

    def online_status(self, isOnline):
        """
        Sets the current chat's online status

        Parameters:
            isOnline (boolean): the value to set this chat's status
        """
        self.online = isOnline

    def write_message(self, message_dict):
        """
        Writes a message to the screen

        Parameters:
            message_dict (dict): The message to write to the screen in dictionary form
        """
        if self.parent.user_id == message_dict["from_id"]:
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
            message_dict["content"]+"\n", (justify_right, "regular_text",))

        if self.parent.user_id == message_dict["from_id"]:
            if (self.online): # if the receiver is online, print 2 ticks
                self.message_box.insert("end",u'\u2713'+u'\u2713'+"\n\n",(justify_right,"regular_text"))

            else: # if the receiver is offline, print 1 tick
                self.message_box.insert("end",u'\u2713'+"\n\n",(justify_right,"regular_text"))
        
        self.message_box.insert("end", "\n", (justify_right, "regular_text",))
        self.message_box.see("end")
    

    def write_messages(self):
        """
        Writes the message history to the chat screen
        """

        self.online = True
        for i, message in enumerate(self.messages):
            self.write_message(message)

        self.online = False

