from fastapi import APIRouter, Depends,status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..user.schemas_user import UserBase
from ..db.database import SessionLocal
from ..db.models import User
from ..depends import get_db_session
from .auth_user import UserUseCases

#cria router de user
routerAuth = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

#faz o post em tbl_usuario pela função create_user de crud
@routerAuth.post("/register")
def user_register(user: UserBase, db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    uc.user_register(user=user)
    return JSONResponse(
        content={'msg': "sucess"},
        status_code=status.HTTP_201_CREATED
    )

    