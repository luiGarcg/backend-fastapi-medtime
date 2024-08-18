from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from typing import List

from . import crud_monitoring, schema_monitoring
from app.db.database import SessionLocal
from ..depends import get_db_session

# Cria router de perfil
routerMedication = APIRouter(
    prefix="/monitoring",
    tags=["monitoring"],
    responses={404: {"description": "Not found"}},
)