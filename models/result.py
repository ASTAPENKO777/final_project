from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)

    team_id = Column(Integer, ForeignKey("teams.id"))
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    team = relationship("Team", back_populates="results")
    tournament = relationship("Tournament", back_populates="results")
