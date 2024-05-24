from .db.database import SessionLocal

def get_db_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()