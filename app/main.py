from fastapi import FastAPI # type: ignore
from app.db.database import engine

from .profile.router_profile import routerProfile
from .auth.router_auth import  routerAuth
from .medication.router_medication import routerMedication
from .time.router_time import routerTime, routerConfirmation
from .time.crud_time import get_time_by_currentTime
from app.db.database import SessionLocal
import asyncio
from app.config import cache


app = FastAPI()

@app.get('/arduino')
def health_check():
    return True

app.include_router(routerProfile)
app.include_router(routerAuth)
app.include_router(routerMedication)
app.include_router(routerTime)
app.include_router(routerConfirmation)

# Função para obter uma sessão do SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def periodic_task():
    while True:
        # Recupera o global_user_id do cache
        global_user_id = await cache.get("global_user_id")
        
        if global_user_id:
            db = SessionLocal()
            try:
                time_ids = get_time_by_currentTime(db, global_user_id)
                if time_ids:
                    print(f"Horários encontrados: {time_ids}")
                else:
                    print("Nenhum horário corresponde ao horário atual")
            finally:
                db.close()  # Fecha a sessão
        else:
            print("Nenhum usuário logado")
        
        await asyncio.sleep(60)  # Espera por 60 segundos antes de repetir
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_task())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)