from fastapi import HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from . import schema_monitoring
from datetime import datetime
from ..db.models import Profile, Monitoring

def get_time(db: Session, per_id:int):
    return db.query(Monitoring).filter(Monitoring.mon_perfilId == per_id).first()

def create_time(db: Session, monitoring: schema_monitoring.MonitoringBase, per_id: int):
    db_user = db.query(Profile).filter(Profile.per_id == per_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="profile not found")
    
    db_profile = Monitoring(
        mon_dataHorario = monitoring.mon_dataHorario,
        mon_perfilId = per_id,
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile
