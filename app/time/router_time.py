from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud_time, schema_time
from app.db.database import SessionLocal
from datetime import datetime, time
from typing import List
import asyncio



# Cria router de perfil
routerTime = APIRouter(
    prefix="/time",
    tags=["time"],
    responses={404: {"description": "Not found"}},
)

# Função para obter uma sessão do SQLAlchemy
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@routerTime.post("/{med_id}", response_model=schema_time.TimeInDB)
def create_time(
    med_id: int,
    time: schema_time.TimeBase,
    db: Session = Depends(get_db_session),
):
    return crud_time.create_time(db=db, time=time, med_id=med_id)

@routerTime.get("/{hor_id}", response_model=schema_time.TimeBase)
def get_time(
    hor_id: int,
    db: Session = Depends(get_db_session),
):
    db_time = crud_time.get_time(db=db, hor_id=hor_id)
    if not db_time:
        raise HTTPException(status_code=404, detail="time not found")
    return db_time

@routerTime.get("/verificar/{per_id}", response_model=List[schema_time.TimeInDB])
def get_time_by_current_time(
    per_id: int,
    db: Session = Depends(get_db_session),
):
    while True:
        return crud_time.get_time_by_currentTime(db=db, per_id=per_id)
    
async def periodic_task(db: Session, per_id: int):
    while True:
        time_ids = crud_time.get_time_by_currentTime(db, per_id)
        if time_ids:
            print(f"Horários encontrados: {time_ids}")
        else:
            print("Nenhum horário corresponde ao horário atual")
        await asyncio.sleep(60)  # Espera por 60 segundos antes de repetir
