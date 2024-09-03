from fastapi import HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from . import schema_monitoring, schema_symptons 
from datetime import datetime
from ..db.models import Profile, Monitoring, Symptoms

def get_monitoring(db: Session, mon_id:int):
    return db.query(Monitoring).filter(Monitoring.mon_id == mon_id).first()

def get_monitoring_by_perId(db: Session, per_id:int):
    return db.query(Monitoring).filter(Monitoring.mon_perfilId == per_id).all()

def get_symptoms(db: Session):
    return db.query(Symptoms).all()

def create_monitoring(db: Session, per_id: int, sin_id: int):
    db_user = db.query(Profile).filter(Profile.per_id == per_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="profile not found")
    db_symptoms = db.query(Symptoms).filter(Symptoms.sin_id == sin_id).first()
    if db_symptoms is None:
        raise HTTPException(status_code=404, detail="symptom  not found")
    
    current_datetime = datetime.now()
    
    db_monitoring = Monitoring(
        mon_sintomasId = db_symptoms.sin_id,
        mon_dataHorario = current_datetime,
        mon_perfilId = db_user.per_id,
    )
    db.add(db_monitoring)
    db.commit()
    db.refresh(db_monitoring)
    return db_monitoring

def create_symptoms(db: Session, symptom: schema_symptons.SymptomsBase):

    db_symptom = Symptoms(
        sin_nome = symptom.sin_nome,
    )
    db.add(db_symptom)
    db.commit()
    db.refresh(db_symptom)
    return db_symptom
