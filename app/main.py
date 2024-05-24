from fastapi import FastAPI
from app.db.database import engine

from app.profile import router_profile
from app.user import router_user
from app.auth import router_auth

app = FastAPI()

@app.get('/')
def health_check():
    return "it's working"

app.include_router(router_user.routerUser)
app.include_router(router_profile.routerProfile)
app.include_router(router_auth.routerAuth)

