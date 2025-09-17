from pydantic import BaseModel, EmailStr, Field
from typing import Optional



class User(BaseModel):
    name: str = Field(...)
    password: str= Field(..., min_length=4, max_length=16)
    email: EmailStr


class UserCreate(BaseModel):
    team_id: Optional[int] = None


class UserRead(BaseModel):
    id: str
    name: str
    email: EmailStr
    team_id : Optional[int]