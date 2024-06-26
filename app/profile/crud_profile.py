from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import schemas_profile
from ..db.models import Profile, User

def get_profiles_perUsuId(db: Session, per_usuId: int):
    return db.query(Profile).filter(Profile.per_usuId == per_usuId).all()

def alter_profile_name(db: Session, per_id: int, profile: schemas_profile.ProfileBase):
    db_profile = db.query(Profile).filter(Profile.per_id == per_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    if profile.per_nome is not None:
        db_profile.per_nome = profile.per_nome

    db.commit()
    db.refresh(db_profile)
    return db_profile

def alter_profile_image(db: Session, per_id: int, profile: schemas_profile.ProfileUpdateImage):
    db_profile = db.query(Profile).filter(Profile.per_id == per_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    if profile.per_foto is not None:
        db_profile.per_foto = profile.per_foto

    db.commit()
    db.refresh(db_profile)
    return db_profile

def create_profile(db: Session, profile: schemas_profile.ProfileBase, usu_id: int):
    db_user = db.query(User).filter(User.usu_id == usu_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    
    db_profile = Profile(per_nome=profile.per_nome, per_usuId = usu_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, per_id: int):
    db_profile = db.query(Profile).filter(Profile.per_id == per_id).first()
    if db_profile:
        db.delete(db_profile)
        db.commit()
        return {"message": "Profile deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Profile not found")