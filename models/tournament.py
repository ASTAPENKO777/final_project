from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    results = relationship("Result", back_populates="tournament")
