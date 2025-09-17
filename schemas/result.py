from pydantic import BaseModel, EmailStr, Field
from typing import List


class Result(BaseModel):
    score: int = Field(..., ge=0)


class ResultCreate(Result):
    team_id: int
    tournament_id: int


class ResultRead(Result):
    id: int
    tournament_id: int
    team_id: int
