from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    email = Column(Text)
    password = Column(Text)
    
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="members")
