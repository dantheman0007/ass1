"""
Defines all the data models used in the chat application
"""

from ipaddress import ip_address
from turtle import back
from xmlrpc.client import boolean
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

# a table that maps the user_id to the chat_id
user_chat = Table(
    "user_chat",
    Base.metadata,
    Column("user_id", String, ForeignKey("user.user_id"), primary_key=True),
    Column("chat_id", String, ForeignKey("chat.chat_id"), primary_key=True)
)



class User(Base):
    '''Class that represents a User table with columns for the user's id, IP address, port number and online status.'''
    __tablename__ = "user"
    user_id = Column(String, primary_key=True)
    ip_address = Column(String)
    server_port = Column(String)
    online_status = Column(Boolean)
    
    chats = relationship("Chat", secondary=user_chat, back_populates="users")

class Message(Base):
    '''Class that represents a Message table with a message id, timestamp that it was sent and the content of the message.'''
    __tablename__ = "message"
    message_id = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    content = Column(String)

    chat_id = Column(String, ForeignKey("chat.chat_id"))
    from_id = Column(String, ForeignKey("user.user_id"))

    def __repr__(self) -> str:
        return self.content

class Chat(Base):
    '''Class that represents a Chat table with an id and name.'''
    __tablename__ = "chat"
    chat_id = Column(String, primary_key=True)
    chat_name = Column(String)

    users  = relationship("User", secondary=user_chat, back_populates="chats")
    messages = relationship("Message")



