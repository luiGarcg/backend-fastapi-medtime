from .db.database import SessionLocal
from .auth.auth_user import UserUseCases
from sqlalchemy.orm import Session
from fastapi import Depends, Request, HTTPException, status

def get_db_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
