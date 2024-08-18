from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud_time, schema_time
from app.db.database import SessionLocal
from datetime import datetime, time
from typing import List
import asyncio
from ..depends import get_db_session


# Cria router de perfil
routerTime = APIRouter(
    prefix="/time",
    tags=["time"],
    responses={404: {"description": "Not found"}},
)

routerConfirmation = APIRouter(
    prefix="/confirmation",
    tags=["confitmation"],
    responses={404: {"description": "Not found"}},
)

@routerTime.post("/{med_id}", response_model=schema_time.TimeInDB)
def create_time(
    med_id: int,
    current_user: str,
    time: schema_time.TimeBase,
    db: Session = Depends(get_db_session),
):
    return crud_time.create_time(db=db, time=time, med_id=med_id)

@routerTime.get("/{hor_id}", response_model=schema_time.TimeBase)
def get_time(
    hor_id: int,
    current_user: str,
    db: Session = Depends(get_db_session),  
):
    db_time = crud_time.get_time(db=db, hor_id=hor_id)
    if not db_time:
        raise HTTPException(status_code=404, detail="time not found")
    return db_time

@routerConfirmation.post("/{clickNotification}", response_model=schema_time.ConfirmationEdit)
def confirm_notification(
    clickNotification: bool,
    current_user: str,
    confirmation: schema_time.ConfirmationEdit,
    db: Session = Depends(get_db_session),  
):
    return crud_time.confirm_notification(db=db, clickNotification=clickNotification, confirmation=confirmation)