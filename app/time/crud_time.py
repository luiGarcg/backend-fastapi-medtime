import asyncio
import threading
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
        # Logar o erro para análise futura
        print(f"Error sending message: {e}")

async def send_reminder_notification(create_new_db_session, fcm_token: str, medication, time_entry, profile_entry, data_payload):
    while True:
        db = create_new_db_session()

        try:
            medication_on_db = db.query(Medication).filter(Medication.med_id == medication.med_id).first()

            if medication_on_db is None:
                print(f"Medication with med_id {medication.med_id} not found in the database.")
                break

            confirmation = db.query(Confirmation).filter(
                Confirmation.con_perfilId == profile_entry.per_id,
                Confirmation.con_medicacaoId == medication.med_id,
                Confirmation.con_horarioId == time_entry.hor_id
            ).first()

            if confirmation and confirmation.con_confirmado:
                print(f"Confirmation already done for con_id: {confirmation.con_id}")
                break
            
            send_notification(
                token=fcm_token,
                title="Lembrete: Tome o medicamento!",
                body=f"Por favor, confirme que você tomou o medicamento {medication.med_nome}.",
                data=data_payload 
            )

        except Exception as e:
            print(f"Error in reminder notification loop: {e}")
        finally:
            db.close()

        await asyncio.sleep(60)

async def get_time_by_currentTime(db: Session, create_new_db_session, usu_id: int):
    user = db.query(Profile).filter(Profile.per_usuId == usu_id).all()
    if not user:
        return []

    matching_times = []
    current_datetime = datetime.now()
    current_time = current_datetime.time().strftime('%H:%M')
    current_date = current_datetime.date()

    for users in user:
        medications = db.query(Medication).filter(Medication.med_perfilId == users.per_id).all()

        for medication in medications:
            medication_date = medication.med_dataFinal

            if current_date > medication_date:
                continue

            times = db.query(Time).filter(Time.hor_medicacao == medication.med_id).all()

            for time_entry in times:
                if time_entry.hor_horario.strftime('%H:%M') == current_time:
                    profile_entry = db.query(Profile).filter(Profile.per_id == medication.med_perfilId).first()
                    user = db.query(User).filter(User.usu_id == profile_entry.per_usuId).first()
                    fcm_token = user.fcm_token if user else None

                    if fcm_token:
                        try:
                            # Criação da confirmação no instante atual
                            db_confirmation = Confirmation(
                                con_medicacaoId=medication.med_id,
                                con_horarioId=time_entry.hor_id,
                                con_perfilId=profile_entry.per_id,
                                con_dataHorario=current_datetime,
                                con_confirmado=False
                            )

                            db.add(db_confirmation)
                            db.commit()
                            db.refresh(db_confirmation)

                            data_payload = {
                                'hor_id': str(time_entry.hor_id),
                                'horario': time_entry.hor_horario.strftime('%H:%M'),
                                'perfil_id': str(profile_entry.per_id),
                                'med_id': str(medication.med_id),
                                'med_nome': str(medication.med_nome),
                                'con_id': str(db_confirmation.con_id)
                            }

                            # Envio da notificação inicial
                            if medication.med_id:
                                send_notification(
                                    token=fcm_token,
                                    title="Hora de tomar o medicamento!",
                                    body=f"É hora de tomar o medicamento {medication.med_nome}.",
                                    data=data_payload 
                                )


                            # Inicia a tarefa assíncrona para enviar lembretes em segundo plano
                            asyncio.create_task(send_reminder_notification(
                                create_new_db_session, fcm_token, medication, time_entry, profile_entry, data_payload
                            ))

                        except Exception as e:
                            # Logar o erro
                            print(f"Error sending notification: {e}")

                    matching_times.append({
                        "hor_id": time_entry.hor_id,
                        "hor_horario": time_entry.hor_horario
                    })

    return matching_times

def confirm_notification(db: Session, con_id: int):
    confirmation = db.query(Confirmation).filter(Confirmation.con_id == con_id).first()

    if confirmation and not confirmation.con_confirmado:
        confirmation.con_confirmado = True
        # Usar datetime completo em vez de apenas o horário
        confirmation.con_dataHorarioConfirmacao = datetime.now()
        db.commit()
        db.refresh(confirmation)
        return confirmation       
    else:
        print("Confirmation not found or already confirmed.")
        return None