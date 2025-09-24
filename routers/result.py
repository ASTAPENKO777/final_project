from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from create_db import get_db
import schemas.result
import models.result
router = APIRouter(prefix='/result', tags=['result'])

@router.post('/', response_model=schemas.result.ResultRead)
def create_result(result: schemas.result.ResultCreate, db: Session = Depends(get_db)):
    db_result = models.result.Result(**result.model_dump())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

@router.get('/', response_model=list[schemas.result.ResultRead])
def read_results(db: Session = Depends(get_db)):
    return db.query(models.result.Result).all()