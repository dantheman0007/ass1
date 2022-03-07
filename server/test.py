from ipaddress import ip_address
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
#print(database.get_users(["123456789"]))