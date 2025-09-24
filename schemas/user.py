from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    name: str = Field(...)
    email: EmailStr


class UserCreate(UserBase):
    password: str= Field(..., min_length=4, max_length=16)
    team_id: Optional[int] = None


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    team_id : Optional[int]

    class Config:
        from_attributes = True
