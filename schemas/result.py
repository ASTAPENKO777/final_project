from pydantic import BaseModel, Field


class Result(BaseModel):
    score: int = Field(..., ge=0)


class ResultCreate(Result):
    team_id: int
    tournament_id: int


class ResultRead(Result):
    id: int
    tournament_id: int
    team_id: int

    class Config:
        from_attributes = True

class ResultWithDetail(ResultRead):
    team_name: str
    tournament_title: str
