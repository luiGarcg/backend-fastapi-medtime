from sqlalchemy import Column, Integer, String

from ..db.database import Base

class User(Base):
    __tablename__ = "tbl_usuario"

    usu_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    usu_email = Column(String,unique=True, nullable=False)
    usu_senha = Column(String, nullable=False)

class Profile(Base):
    __tablename__="tbl_perfil"

    per_id = Column(Integer, primary_key=True, autoincrement=True)
    per_nome = Column(String, index=True)
    per_usuId = Column(Integer, index=True)
    per_foto = Column(String, index=True, default="/default.png")
