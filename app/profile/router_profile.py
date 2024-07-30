from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud_profile, schemas_profile
from app.db.database import SessionLocal

# Cria router de perfil
routerProfile = APIRouter(
    prefix="/profile",
    tags=["profile"],
    responses={404: {"description": "Not found"}},
)

# Função para obter uma sessão do SQLAlchemy
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@routerProfile.post("/{usu_id}", response_model=schemas_profile.ProfileBase)
def create_profile(
    usu_id: int,
    profile: schemas_profile.ProfileBase,
    db: Session = Depends(get_db_session),
):
    return crud_profile.create_profile(db=db, profile=profile, usu_id=usu_id)

@routerProfile.patch("/alterName/{per_id}", response_model=schemas_profile.ProfileBase)
def alter_profile_name(
    per_id: int,
    profile: schemas_profile.ProfileBase,
    db: Session = Depends(get_db_session),
):
    return crud_profile.alter_profile_name(db=db, profile=profile,per_id=per_id)

@routerProfile.patch("/alterImage/{per_id}", response_model=schemas_profile.ProfileUpdateImage)
def alter_profile_image(
    per_id: int,
    profile: schemas_profile.ProfileUpdateImage,
    db: Session = Depends(get_db_session),
):
    return crud_profile.alter_profile_image(db=db, profile=profile,per_id=per_id)

@routerProfile.get("/{per_usuId}", response_model=List[schemas_profile.Profile])
def get_profiles_perUsuId(
    per_usuId: int,
    db: Session = Depends(get_db_session),
):
    db_profiles = crud_profile.get_profiles_perUsuId(db=db, per_usuId=per_usuId)
    if not db_profiles:
        raise HTTPException(status_code=404, detail="Profiles not found")
    return db_profiles

@routerProfile.delete("/{per_id}", response_model=dict)
def delete_profile(
    per_id: int,
    db: Session = Depends(get_db_session),
):
    return crud_profile.delete_profile(db=db, per_id=per_id)
