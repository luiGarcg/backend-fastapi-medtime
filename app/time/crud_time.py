from fastapi import HTTPException # type: ignore
from datetime import datetime
from sqlalchemy.orm import Session # type: ignore
from . import schema_time
from ..db.models import Time, Medication, Profile, Confirmation
from typing import List, Dict

def get_time(db: Session, hor_id:int):
    return db.query(Time).filter(Time.hor_id == hor_id).first()

def create_time(db: Session, time: schema_time.TimeBase, med_id: int):
    db_user = db.query(Medication).filter(Medication.med_id == med_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="medication not found")
    
    db_time = Time(
        hor_horario = time.hor_horario,
        hor_medicacao = med_id
    )
    db.add(db_time)
    db.commit()
    db.refresh(db_time)
    return db_time


def get_time_by_currentTime(db: Session, usu_id: int) -> List[Dict]:
    user = db.query(Profile).filter(Profile.per_usuId == usu_id).all()
    if not user:
        return []

    matching_times = []

    for users in user:
        profiles = db.query(Medication).filter(Medication.med_perfilId == users.per_id).all()
        current_time = datetime.now().time()
        current_date = datetime.now().date()

        for profile in profiles:
            # Supondo que a data relevante esteja armazenada como `med_data` no modelo Medication
            medication_date = profile.med_dataFinal  # Substitua pelo nome correto do campo de data no modelo Medication
            
            # Verifica se a data do medicamento já passou
            if current_date > medication_date:
                continue

            times = db.query(Time).filter(Time.hor_medicacao == profile.med_id).all()

            for time in times:
                if time.hor_horario.strftime('%H:%M') == current_time.strftime('%H:%M'):
                    matching_times.append({
                        "hor_id": time.hor_id,
                        "hor_horario": time.hor_horario,
                        "med_id": time.hor_medicacao,
                        "per_id": users.per_id
                    })

    return matching_times

def confirm_notification(db: Session, clickNotification: bool, confirmation: schema_time.ConfirmationEdit):
    medication = db.query(Medication).filter(Medication.med_id == confirmation.con_medicacaoId).first()
    time = db.query(Time).filter(Time.hor_id == confirmation.con_horarioId).first()
    current_time = datetime.now()

    if clickNotification:
        db_confirmation = Confirmation(con_medicacaoId=medication.med_id, con_horarioId = time.hor_id, con_dataHorario = current_time)
        db.add(db_confirmation)
        db.commit()
        db.refresh(db_confirmation)
        return db_confirmation
