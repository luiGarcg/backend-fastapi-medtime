from fastapi import FastAPI
from app.db.database import engine

from .profile.router_profile import routerProfile
from .user.router_user import routerUser
from .auth.router_auth import  routerAuth, routerTest

app = FastAPI()


@app.get('/arduino')
def health_check():
    return True

app.include_router(routerUser)
app.include_router(routerProfile)
app.include_router(routerAuth)
app.include_router(routerTest)


