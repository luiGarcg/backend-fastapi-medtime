from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud_medication, schema_medication
from app.db.database import SessionLocal
from ..depends import get_db_session

# Cria router de perfil
routerMedication = APIRouter(
    prefix="/medication",
    tags=["medication"],
    responses={404: {"description": "Not found"}},
)

@routerMedication.post("/{per_id}", response_model=schema_medication.MedicationInDB)
def create_medication(
    per_id: int,
    current_user: str,
    medication: schema_medication.MedicationBase,
    db: Session = Depends(get_db_session),  
):
    return crud_medication.create_medication(db=db, medication=medication, per_id=per_id)

@routerMedication.get("/{med_id}", response_model=schema_medication.MedicationBase)
def get_medication(
    med_id: int,
    current_user: str,
    db: Session = Depends(get_db_session),
):
    db_profiles = crud_medication.get_medication(db=db, med_id=med_id)
    if not db_profiles:
        raise HTTPException(status_code=404, detail="Profiles not found")
    return db_profiles

