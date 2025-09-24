from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from .base import Base


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)

    members = relationship("User", back_populates="team")
    result = relationship("Result", back_populates="team")
