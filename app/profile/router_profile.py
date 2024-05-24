from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud_profile, schemas_profile
from app.db.database import SessionLocal
from ..depends import get_db_session

#cria router de user
routerProfile = APIRouter(
    prefix="/profile",
    tags=["profile"],
    responses={404: {"description": "Not found"}},
)

#faz o post em tbl_usuario pela função create_user de crud
@routerProfile.post("/", response_model=schemas_profile.Profile)
def create_profile(profile: schemas_profile.ProfileCreate, db: Session = Depends(get_db_session)):
    return crud_profile.create_profile(db=db, profile=profile)

#faz o get em tbl_usuario pela função get_user de crud
@routerProfile.get("/{per_id}", response_model=schemas_profile.Profile)
def get_profile(per_id: int, db: Session = Depends(get_db_session)):
    db_profile = crud_profile.get_profile(db=db, per_id=per_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="profile not found")
    return db_profile

