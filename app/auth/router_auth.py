from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.models import User
from ..user.schemas_user import UserBase
from ..depends import get_db_session
from .auth_user import UserUseCases
from .schemas_auth import LoginSchema, AuthSignUp
from typing import Optional

# Cria router de auth
routerAuth = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# Cria router de test
routerTest = APIRouter(
    prefix='/test', 
)

# Função para verificar se o email já está registrado
def is_email_registered(db_session: Session, email: str) -> bool:
    user_on_db = db_session.query(User).filter_by(usu_email=email).first()
    return user_on_db is not None

# Faz o post em tbl_usuario pela função create_user de crud
@routerAuth.post("/register")
def user_register(user: AuthSignUp, db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    uc.user_register(user=user)
    return JSONResponse(
        content={'msg': "success"},
        status_code=status.HTTP_201_CREATED
    )

@routerAuth.post("/login")
def user_login(request_form_user: LoginSchema, db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    user = UserBase(
        usu_email=request_form_user.usu_email,
        usu_senha=request_form_user.usu_senha
    )
    auth_data = uc.user_login(user=user)

    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_200_OK
    )

@routerTest.post("/test")
def test_user_verify(token: Optional[str] = None, db_session: Session = Depends(get_db_session)):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Token is required'
        )

    user_use_case = UserUseCases(db_session)
    try:
        user_use_case.verify_token(token)
        return {"message": "Token is valid"}
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
