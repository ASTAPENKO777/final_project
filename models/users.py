from sqlalchemy import Table, Column, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    email = Column(Text)
    password = Column(Text)
