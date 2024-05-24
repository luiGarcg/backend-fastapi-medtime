from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud_user, schemas_user
from app.db.database import SessionLocal
from ..depends import get_db_session

#cria router de user
routerUser = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


#faz o post em tbl_usuario pela função create_user de crud
@routerUser.post("/", response_model=schemas_user.User)
def create_user(user: schemas_user.UserCreate, db: Session = Depends(get_db_session)):
    return crud_user.create_user(db=db, user=user)

#faz o get em tbl_usuario pela função get_user de crud
@routerUser.get("/{usu_id}", response_model=schemas_user.User)
def get_user(usu_id: int, db: Session = Depends(get_db_session)):
    db_item = crud_user.get_user(db=db, usu_id=usu_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_item

