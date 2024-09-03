from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from typing import List

from . import crud_monitoring, schema_monitoring, schema_symptons
from app.db.database import SessionLocal
from ..depends import get_db_session

# Cria router de perfil
routerMonitoring = APIRouter(
    prefix="/monitoring",
    tags=["monitoring"],
    responses={404: {"description": "Not found"}},
)

@routerMonitoring.post("/", response_model=schema_monitoring.MonitoringBase)
def create_monitoring(
    per_id: int,
    sin_id: int,
    db: Session = Depends(get_db_session),

):
    return crud_monitoring.create_monitoring(db=db, per_id=per_id, sin_id=sin_id)

@routerMonitoring.post("/symptom", response_model=schema_symptons.SymptomsBase)
def create_symptoms(
    symptom: schema_symptons.SymptomsBase,
    db: Session = Depends(get_db_session),

):
    return crud_monitoring.create_symptoms(db=db, symptom=symptom)

@routerMonitoring.get("/{mon_id}", response_model=schema_monitoring.MonitoringEdit)
def get_monitoring(
    mon_id: int,
    db: Session = Depends(get_db_session),

):
    db_monitoring = crud_monitoring.get_monitoring(db=db, mon_id=mon_id)
    if not db_monitoring:
        raise HTTPException(status_code=404, detail="monitoring not found")
    return db_monitoring


@routerMonitoring.get("/byPerId/{per_id}", response_model=List[schema_monitoring.MonitoringEdit])
def get_monitoring_by_perId(
    per_id: int,
    db: Session = Depends(get_db_session),
):
    monitorings = crud_monitoring.get_monitoring_by_perId(db=db, per_id=per_id)
    if not monitorings:
        raise HTTPException(status_code=404, detail="monitoring not found")
    return [schema_monitoring.MonitoringEdit.from_orm(monitoring) for monitoring in monitorings]

@routerMonitoring.get("/", response_model=List[schema_symptons.SymptomsBase])
def get_symtoms(
    db: Session = Depends(get_db_session),
):
    symptoms = crud_monitoring.get_symptoms(db=db)
    return [schema_symptons.SymptomsInBD.model_validate(symptom) for symptom in symptoms]

