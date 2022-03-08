'''from ipaddress import ip_address
import db 
import models

id = input("Input your username: ")
ip = input('Enter you IP address: ')

database = db.DB()

database.create_or_update(models.User, [{
        "user_id": id,
        "ip_address": ip
    }], "user_id")

print(database.get_record_from_pk(models.User, id))
print((database.get_record_from_pk(models.User, id)).user_id)
print(database.get_record_from_pk(models.User, "123456789")) 
#print(database.get_users(["123456789"]))'''

import db 
from datetime import datetime 
database = db.DB()
database.add_message("MRRJUL007-MRRMAT001", "sup", datetime.now(), "MRRJUL007")
#print(database.get_chat_messages("MRRJUL007-MRRMAT001"))

print()
msgs = []

for msg in database.get_chat_messages(chat_id="MRRJUL007-MRRMAT001"):
    msg_dict = {
        "message_id": msg.message_id,
        "msg_content": msg.content,
        "timestamp": datetime.strftime(msg.timestamp, "%d/%m/%Y at %H:%M:%S"),
        "from_id": msg.from_id
    }
    msgs.append(msg_dict)
    #print("Message to {} from {} at {}: \n {}".format(msg.chat_id, msg.from_id, msg.timestamp, msg.content))
print(msgs)