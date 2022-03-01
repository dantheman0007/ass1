import sqlalchemy as sq
import models
import uuid

class DB():

    DATABASE_NAME = "chatdb.sqlite"

    def __init__(self):
        self.engine = sq.create_engine("sqlite:///{}".format(self.DATABASE_NAME), echo = True)

        self.connection = self.engine.connect()
        
        Session = sq.orm.sessionmaker()
        Session.configure(bind = self.engine)
        self.session = Session()
        pass

    

    def add_user(self, values):
        query = sq.insert(models.User)
        ResultProxy = self.connection.execute(query, values)

    def create_or_update(self, model, values, pk):
        for value in values:
            print(value)
            instance = self.session.query(model).get(pk)

            if instance:
                #update??
                pass
            else:
                instance = model(**value) 
                self.session.add(instance)
                self.session.commit()


    def add_message(self, chat_id, content, timestamp, from_id):
        msg_data =[
            {
                "message_id": str(uuid.uuid4()),
                "content": content,
                "timestamp": timestamp,
                "chat_id": chat_id,
                "from_id": from_id,
            }
        ]

        self.create_or_update(models.Message, msg_data, "message_id")

    def get_chat_messages(self, chat_id):
        messages = self.session.query(models.Message).filter_by(chat_id = chat_id).order_by(models.Message.timestamp)

        return messages