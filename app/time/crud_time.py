from fastapi import HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import schema_time
from ..db.models import Confirmation, Time, Medication, User, Profile
from firebase_admin import messaging
import time

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
        current_datetime = datetime.now()
        current_time = current_datetime.time().strftime('%H:%M')
        current_date = current_datetime.date()
        print(f"Current time: {current_time}")

        for medication in medications:
            medication_date = medication.med_dataFinal

            if current_date > medication_date:
                continue

            print(f"Checking medication: {medication.med_id}")

            times = db.query(Time).filter(Time.hor_medicacao == medication.med_id).all()

            for time_entry in times:
                print(f"Checking time: {time_entry.hor_horario.strftime('%H:%M')}")

                if time_entry.hor_horario.strftime('%H:%M') == current_time:
                    print(f"Match found for time: {time_entry.hor_horario.strftime('%H:%M')}")

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
                                'hor_id': str(time_entry.hor_id),
                                'horario': time_entry.hor_horario.strftime('%H:%M'),
                                'perfil_id': str(profile_entry.per_id),
                                'med_id': str(medication.med_id),
                                'med_nome': str(medication.med_nome)
                            }

                            db_confirmation = Confirmation(
                                con_medicacaoId=medication.med_id,
                                con_horarioId=time_entry.hor_id,
                                con_perfilId=profile_entry.per_id,
                                con_dataHorario=current_datetime,  # Use datetime
                                con_confirmado=False
                            )
                            db.add(db_confirmation)
                            db.commit()
                            db.refresh(db_confirmation)
                            
                            send_notification(
                                token=fcm_token,
                                title="Hora de tomar o medicamento!",
                                body=f"É hora de tomar o medicamento {medication.med_nome}.",
                                data=data_payload 
                            )
                            print("Notification sent successfully")

                            while not db_confirmation.con_confirmado:
                                time.sleep(60)  # Aguarde 1 minuto antes de enviar novamente
                                send_notification(
                                    token=fcm_token,
                                    title="Lembrete: Tome o medicamento!",
                                    body=f"Por favor, confirme que você tomou o medicamento {medication.med_nome}.",
                                    data=data_payload 
                                )
                                # Atualize a confirmação do banco de dados
                                db_confirmation = db.query(Confirmation).filter(Confirmation.con_id == db_confirmation.con_id).first()
                        except Exception as e:
                            print(f"Error sending notification: {e}")
                    else:
                        print("FCM Token is None")
                
                    matching_times.append({
                        "hor_id": time_entry.hor_id,
                        "hor_horario": time_entry.hor_horario
                    })

    return matching_times

def confirm_notification(db: Session, con_id:int):
    confirmation = db.query(Confirmation).filter(Confirmation.con_id == con_id).first()

    if confirmation and not confirmation.con_confirmado:
        confirmation.con_confirmado = True
        confirmation.con_dataHorarioConfirmacao = datetime.now().time().strftime('%H:%M')
        db.commit()
        db.refresh(confirmation)
        return confirmation       
    else:
        print("Confirmation not found or already confirmed.")
        return None
