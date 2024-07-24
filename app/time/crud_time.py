from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from . import schema_time
from ..db.models import Time, Medication

def get_time(db: Session, hor_id:int):
    return db.query(Time).filter(Time.hor_id == hor_id).first()

def create_time(db: Session, time: schema_time.TimeBase, med_id: int):
    db_user = db.query(Medication).filter(Medication.med_id == med_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="medication not found")
    
    db_profile = Time(
        hor_horario = time.hor_horario,
        hor_medicacao = med_id
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_time_by_currentTime(db: Session, per_id: int):
    profiles =  db.query(Medication).filter(Medication.med_perfilId == per_id).all()
    current_time = datetime.now().time()

    matching_times = []

    for profile in profiles:
        times =  db.query(Time).filter(Time.hor_medicacao == profile.med_id).all()

        for time in times:
            if time.hor_horario.strftime('%H:%M') == current_time.strftime('%H:%M'):
                matching_times.append({
                    "hor_id": time.hor_id,
                    "hor_horario": time.hor_horario
                })
    return matching_times