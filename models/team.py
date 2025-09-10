from sqlalchemy import Table, Column, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    quantity_players = Column(Integer)
