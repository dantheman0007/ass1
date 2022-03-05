from re import search
import sqlalchemy as sq
import models
import uuid


class DB():
    """
    Database interface class

    Exposes methods that are used to interact with the sqlite database
    """

    DATABASE_NAME = "chatdb.sqlite"

    def __init__(self):
        """Initiates a connection with the database and starts a session"""
        self.engine = sq.create_engine("sqlite:///{}".format(self.DATABASE_NAME), echo = True)

        self.connection = self.engine.connect()
        
        Session = sq.orm.sessionmaker()
        Session.configure(bind = self.engine)
        self.session = Session()


    def create_or_update(self, model, values, pk):
        """
        Generic method to create or update any record in any model and return an instance of that record.

        Also works for batch insertions or updates, in which case the last record of the batch job is returned.

        Parameters:
            model: the model (or table) in which to perform the Create or Update task
            values: a list of dictionaries specifying the values the new record should contain
            pk: the primary key of this table, as a string
        """


        for value in values:

            instance = self.session.query(model).get(value[pk])
            
            if instance is not None:

                instance = self.session.merge(model(**value))
                self.session.commit()

            else:
                instance = model(**value) 
                self.session.add(instance)
                self.session.commit()


        return instance


    def set_ip(self, user_id, new_ip):
        """
        Sets the IP address of a user

        Parameters:
            user_id: The primary key of the user to update the ip of
            new_ip: The new ip address
        """

        user = self.session.query(models.User).get(user_id)
        user.ip_address = new_ip
        self.session.commit()

    def add_message(self, chat_id, content, timestamp, from_id):
        """
        Adds a new message record and assigns it a unique ID

        This is essentially a wrapper for the create_or_update method.

        Parameters:
            chat_id: the id of the chat the message was sent to
            content: the actual message content
            timestamp: the time the message was received on the server
            from_id: the id of the user sending the message
        """

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
        """
        Returns all the messages associated with a chat_id, in order of timestamp

        Parameters:
            chat_id: the id of the chat to get the messages from
        """

        messages = self.session.query(models.Message).filter_by(chat_id = chat_id).order_by(models.Message.timestamp)

        return messages

    def get_record_from_pk(self, model, pk):
        """
        Generic method to get any record from the database from its primary key. Returns an instance of the specified model

        Parameters:
            model: the model to get the record from 
            pk: the value of the primary key
        """
        return self.session.query(model).get(pk)

    def get_records(self, model, search_fields):
        """
        Generic wrapper to perform a basic SELECT quesry on any model.

        Returns a list of model instances (where 1+ results were found) or None if no results matched the query

        Parameters:
            model: the model to perform the query on
            search_fields: a dictionary of key-value paris for the WHERE clause of the 

        """

        return self.session.query(model).filter_by(**search_fields)

    def get_users(self, ids):
        """
        Returns a list of User instances whose user_ids are in the ids list
        
        Parameters:
            ids (list): a list of user id strings

        Returns:
            A list of User instances if User.user_id is in ids or None if there are no users with the id in ids

        """
        return self.session.query(models.User).filter(models.User.user_id.in_(ids))


    def get_chats_from_user(self, users):
        """
        Fetches a chat based on its participantss

        Parameters:
            users (list): a list of User instances
        
        Returns:
            A list of chat instances
        """

        chat = self.session.query(models.Chat).filter(users = users)

