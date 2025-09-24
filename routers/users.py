from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from create_db import get_db
import schemas.user
import models.user

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', response_model=schemas.user.UserRead)
def create_user(user: schemas.user.UserCreate, db: Session=Depends(get_db)):
    db_user = models.user.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
