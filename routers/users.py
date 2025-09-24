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


@router.get('/', response_model=list[schemas.user.UserRead])
def all_users(db: Session = Depends(get_db)):
    return db.query(models.user.User).all()


@router.get('/{user_id}', response_model=schemas.user.UserRead)
def one_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user
