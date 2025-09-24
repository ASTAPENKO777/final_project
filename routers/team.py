from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from create_db import get_db
import schemas.team
import models.team
router = APIRouter(prefix='/team', tags=['Team'])


@router.post('/', response_model=schemas.team.TeamRead)
def create_team(team: schemas.team.Team, db: Session = Depends(get_db)):
    db_team = models.team.Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.get('/', response_model=list[schemas.team.TeamRead])
def all_teams(db: Session = Depends(get_db)):
    return db.query(models.team.Team).all()


@router.get('/{team_id}', response_model=schemas.team.TeamRead)
def one_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.team.Team).filter(models.team.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail='Team not found')
    return team
