from sqlalchemy.orm import Session
from . import schemas_user
from ..db.models import User

#faz a busca de dados na tabela tbl_usuario
def get_user(db: Session, usu_id: int):
    return db.query(User).filter(User.usu_id == usu_id).first()

#adiciona novos dados na tabela tbl_usuario
def create_user(db: Session, user: schemas_user.UserCreate):
    db_user = User(usu_email=user.usu_email, usu_senha=user.usu_senha)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
