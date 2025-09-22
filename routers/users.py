from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import users
from data_base import get_db
from schemas import user
import schemas.user

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', response_model=schemas.user.UserRead)
def create_user(user: users.UserCreate, db: Session=Depends(get_db)):
    db_user = users.Users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
