from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Tournament(BaseModel):
    title: str = Field(...)
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None


class TournamentRead(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True