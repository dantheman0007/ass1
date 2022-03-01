import argparse

from numpy import record
import models
import os
import sqlalchemy as sq
import db
import pandas as pd
import uuid
from datetime import datetime

DATABASE_NAME = "chatdb.sqlite"

def create_new_db():
    print("Deleting old database file...")

    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        
    print("Creating new db")
    engine = sq.create_engine("sqlite:///{}".format(DATABASE_NAME), echo=True)
    connection = engine.connect()

    print("Creating tables")
    models.Base.metadata.create_all(engine)

    print("DONE")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("command")
    
    args = parser.parse_args()
   
    if args.command == "create_db":
        create_new_db()

    elif args.command == "add_users":
        
        database = db.DB()
        users = pd.read_excel("data/user_data.xlsx")
        
        database.create_or_update(models.User, users.to_dict("records"), "user_id")

    elif args.command == "add_chats":

        database = db.DB()
        chats = pd.read_excel("data/chat_data.xlsx")
        
        database.create_or_update(models.Chat, chats.to_dict("records"), "chat_id")

    elif args.command == "add_messages":
        database = db.DB()

        while True:
            chat_id = input("Chat Id: ")
            from_id = input("Your ID: ")
            
            timestamp = datetime.now()
            print("Timestamp: {}".format(timestamp))

            content = input("Message: ")

            input("Press enter to send")

            database.add_message(chat_id, content, timestamp, from_id)
    elif args.command == "get_messages":
        chat_id = input("Chat id: ")

        database = db.DB()

        print()

        for msg in database.get_chat_messages(chat_id=chat_id):
            print("Message to {} from {} at {}: \n {}".format(msg.chat_id, msg.from_id, msg.timestamp, msg.content))
            

            


    pass
