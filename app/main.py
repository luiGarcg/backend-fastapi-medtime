from fastapi import FastAPI  # type: ignore
from app.db.database import engine

from .profile.router_profile import routerProfile
from .auth.router_auth import routerAuth
from .medication.router_medication import routerMedication
from .time.router_time import routerTime, routerConfirmation
from .monitoring.router_monitoring import routerMonitoring
from .time.crud_time import get_time_by_currentTime
from app.db.database import SessionLocal
import asyncio
from app.config import cache

import firebase_admin
from firebase_admin import credentials
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Carregar as credenciais do Firebase a partir da variável de ambiente
credentials_json = os.getenv('GOOGLE_CREDENTIALS')
if credentials_json:
    cred = credentials.Certificate(json.loads(credentials_json))
    firebase_admin.initialize_app(cred)
else:
    raise ValueError("Credenciais do Firebase não encontradas. Certifique-se de que a variável de ambiente 'GOOGLE_CREDENTIALS' está configurada.")

app = FastAPI()

@app.get('/arduino')
def health_check():
    return True

app.include_router(routerProfile)
app.include_router(routerAuth)
app.include_router(routerMedication)
app.include_router(routerTime)
app.include_router(routerConfirmation)
app.include_router(routerMonitoring)

# Função para obter uma sessão do SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def periodic_task():
    while True:
        global_user_id = await cache.get("global_user_id")
        
        if global_user_id:
            db = SessionLocal()
            try:
                time_ids = await get_time_by_currentTime(db, SessionLocal, global_user_id)
                if time_ids:
                    print(f"Horários encontrados: {time_ids}")
                else:
                    print("Nenhum horário corresponde ao horário atual")
            except Exception as e:
                print(f"Erro na periodic_task: {e}")
            finally:
                db.close()  # Fecha a sessão
        else:
            print("Nenhum usuário logado")
        
        await asyncio.sleep(60)  # Espera por 60 segundos antes de repetir
        
@app.on_event("startup")
async def startup_event():
    logging.info("Iniciando a aplicação...")
    asyncio.create_task(periodic_task())
