from tkinter import *
from tkinter import ttk
from functools import partial

class HomeScreen(object):


        def __init__(self, parent) -> None:

            self.parent = parent
            self.root = Toplevel(parent.root)
            self.root.protocol("WM_DELETE_WINDOW", self.log_out)

            self.chats = self.parent.chats
            print("Home: ", self.chats)
            self.root.title("Home")
            self.root.geometry("550x400+300+300")
            

            self.draw_gui()
            
            pass


        def log_out(self):
            self.parent.client.log_out()
            self.parent.root.destroy()

        
        def draw_gui(self):
            self.mainframe = ttk.Frame(self.root, padding = 10)
            self.mainframe.grid(column=0, row=0)
            self.chats_frame = ttk.Frame(self.mainframe, padding = 10)
            self.chats_frame.grid(row=2, column=0, padx=200)

            frames = []
            self.labels = dict()

            ttk.Label(self.mainframe, text = "Chats for {}".format(self.parent.user_id)).grid(row=1, column = 0)

            btn_new_chat = ttk.Button(self.chats_frame, text = "New Chat", command = self.new_chat_window)

            btn_new_chat.grid(row = 0, column= 4)

            btn_refresh = ttk.Button(self.chats_frame, text = "Refresh", command = self.redraw_chat_frame)

            btn_refresh.grid(row = 0, column= 5)

            for i, chat in enumerate(self.parent.chats):

                f = ttk.Frame(self.chats_frame, relief="solid", borderwidth=5, width=200, height= 100, padding=10)
                f.grid(row = i+1, column =4, columnspan=4, sticky=(E, W) ,pady=5)
                
                cid = chat["chat_id"].split("-")
                cid.remove(self.parent.user_id)

                if len(cid) > 1:
                    cid = " - ".join(cid)

                
                l = ttk.Label(f, text = cid)
                
                l.grid(row = i, column =0,sticky=W)

                f.bind("<Button-1>", partial(self.parent.fetch_messages, chat["chat_id"]))
                l.bind("<Button-1>", partial(self.parent.fetch_messages, chat["chat_id"]))

                self.labels[chat["chat_id"]] = l
    
                frames.append(f)

                pass


        def new_chat_window(self, *args):
            top= Toplevel(self.root)
            top.geometry("350x150+300+300")
            top.title("NEW MESSAGE")

            lbl = ttk.Label(top, text="Enter the list of users you want to talk to, separated by a space:", wraplength=150)
            lbl.pack(pady=5 )

            entry= Entry(top, width= 50)
            entry.pack()
            entry.bind("<Return>",  lambda x:self.close_win(top, entry))

            button= Button(top, text="Ok", command=lambda:self.close_win(top, entry))
            button.pack(pady=5, side= TOP)

            entry.focus()

        def error_window(self, err):
            top= Toplevel(self.root)
            top.geometry("350x150+300+300")
            # set location
            top.title("ERROR")

            lbl = ttk.Label(top, text= err, wraplength=150)
            lbl.pack(pady=5 )

        def update_unreads(self, chat_id):
            print(self.labels[chat_id].cget("text"))

        def close_win(self, top, entry):
            
            users = entry.get().split()
            users.append(self.parent.user_id)
            self.parent.client.new_chat(users)
            top.destroy()
            self.redraw_chat_frame()
            

        def redraw_chat_frame(self, *args):
            self.parent.client.refresh_chats()
            self.chats_frame.grid_forget()
            self.draw_gui()
