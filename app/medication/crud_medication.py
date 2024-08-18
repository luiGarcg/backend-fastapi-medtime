from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import schema_medication
from datetime import datetime
from ..db.models import Medication, Profile

def get_medication(db: Session, med_id:int):
    return db.query(Medication).filter(Medication.med_id == med_id).first()

def create_medication(db: Session, medication: schema_medication.MedicationBase, per_id: int):
    db_user = db.query(Profile).filter(Profile.per_id == per_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="profile not found")
    
    db_profile = Medication(
        med_nome=medication.med_nome, 
        med_descricao=medication.med_descricao,
        med_tipo=medication.med_tipo,
        med_quantidade=medication.med_quantidade, 
        med_dataInicio=medication.med_dataInicio,
        med_dataFinal=medication.med_dataFinal,
        med_perfilId=per_id, 
        med_estado=medication.med_estado
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile
