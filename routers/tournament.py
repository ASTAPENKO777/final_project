from sys import prefix

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from create_db import get_db
import schemas.tournament
import models.tournament



router = APIRouter(prefix="/tournaments", tags=["Tournaments"])
@router.post("/", response_model=schemas.tournament.TournamentRead)
def create_tournament(tournament:schemas.tournament.Tournament, db: Session=Depends(get_db)):
    db_tournament = models.tournament.Tournament(**tournament.dict())
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament()

@router.get("/", response_model=list[schemas.tournament.TournamentRead])
def get_tournaments(db: Session=Depends(get_db)):
    return db.query(models.tournament.Tournament).all()

