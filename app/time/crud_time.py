from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from . import schema_time
from ..db.models import Confirmation, Time, Medication, User, Profile
from firebase_admin import messaging


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

def send_notification(token: str, title: str, body: str, data: dict):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token,
        data=data
    )

    try:
        response = messaging.send(message)
        print(f"Successfully sent message: {response}")
    except Exception as e:
        print(f"Error sending message: {e}")

def get_time_by_currentTime(db: Session, usu_id: int):
    user = db.query(Profile).filter(Profile.per_usuId == usu_id).all()
    if not user:
        return []
    
    matching_times = []

    for users in user:        
        medications = db.query(Medication).filter(Medication.med_perfilId == users.per_id).all()
        current_time = datetime.now().time().strftime('%H:%M')
        current_date = datetime.now().date()
        print(f"Current time: {current_time}")

        for medication in medications:
            medication_date = medication.med_dataFinal 
            
            if current_date > medication_date:
                continue

            print(f"Checking medication: {medication.med_id}")

            times = db.query(Time).filter(Time.hor_medicacao == medication.med_id).all()

            for time in times:
                print(f"Checking time: {time.hor_horario.strftime('%H:%M')}")

                if time.hor_horario.strftime('%H:%M') == current_time:
                    print(f"Match found for time: {time.hor_horario.strftime('%H:%M')}")

                    profile_entry = db.query(Profile).filter(Profile.per_id == medication.med_perfilId).first()
                    if profile_entry:
                        print(f"Profile found: {profile_entry.per_id}")

                        user = db.query(User).filter(User.usu_id == profile_entry.per_usuId).first()
                        if user:
                            print(f"User found: {user.usu_id}")
                            fcm_token = user.fcm_token
                            print(f"FCM Token: {fcm_token}")
                        else:
                            fcm_token = None
                            print("User not found for profile")
                    else:
                        fcm_token = None
                        print("Profile not found for medication")

                    if fcm_token:
                        try:
                            data_payload = {
                                'hor_id': str(time.hor_id),
                                'horario': time.hor_horario.strftime('%H:%M'),
                                'perfil_id': str(profile_entry.per_id),
                                'med_id': str(medication.med_id),
                                'med_nome': str(medication.med_nome),
                            }
                            send_notification(
                                token=fcm_token,
                                title="Hora de tomar o medicamento!",
                                body=f"É hora de tomar o medicamento {medication.med_nome}.",
                                data=data_payload 
                            )
                            print("Notification sent successfully")
                        except Exception as e:
                            print(f"Error sending notification: {e}")
                    else:
                        print("FCM Token is None")
                
                    matching_times.append({
                        "hor_id": time.hor_id,
                        "hor_horario": time.hor_horario
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
