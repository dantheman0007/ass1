"""
Defines all the data models used in the chat application
"""

from ipaddress import ip_address
from turtle import back
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

user_chat = Table(
    "user_chat",
    Base.metadata,
    Column("user_id", String, ForeignKey("user.user_id"), primary_key=True),
    Column("chat_id", String, ForeignKey("chat.chat_id"), primary_key=True)
)



class User(Base):
    __tablename__ = "user"
    user_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    ip_address = Column(String)
    
    chats = relationship("Chat", secondary=user_chat, back_populates="users")

class Message(Base):
    __tablename__ = "message"
    message_id = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    content = Column(String)

    chat_id = Column(String, ForeignKey("chat.chat_id"))
    from_id = Column(String, ForeignKey("user.user_id"))

    def __repr__(self) -> str:
        return self.content

class Chat(Base):
    __tablename__ = "chat"
    chat_id = Column(String, primary_key=True)
    chat_name = Column(String)

    users  = relationship("User", secondary=user_chat, back_populates="chats")
    messages = relationship("Message")



