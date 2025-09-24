from pydantic import BaseModel, Field
from typing import List

from schemas.user import UserRead


class Team(BaseModel):
    name: str = Field(...)


class TeamRead(BaseModel):
    id: int
    name: str
    members: List[UserRead] = []

    class Config:
        from_attributes = True
