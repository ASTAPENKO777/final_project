from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from create_db import get_db
import schemas.result
import models.result
import schemas.team
import models.team
import schemas.tournament
import models.tournament
router = APIRouter(prefix='/result', tags=['Result'])

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

@router.get('/best', response_model=schemas.result.ResultWithDetail)
def best_result(db: Session = Depends(get_db)):
    best = (
        db.query(models.result.Result)
        .join(models.team.Team, models.team.Team.id == models.result.Result.team_id)
        .join(models.tournament.Tournament, models.tournament.Tournament.id == models.result.Result.tournament_id)
        .order_by(models.result.Result.score.desc())
        .first()
        )
    if not best:
        raise HTTPException(status_code=404, detail='not found')
    return {
        'id': best.id,
        'score': best.score,
        'team id': best.team_id,
        'tournament id': best.tournament_id,
        'team name': best.team.name,
        'tournament title': best.tournament.title
    }
