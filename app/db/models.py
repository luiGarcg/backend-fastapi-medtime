from sqlalchemy import Column, Integer, String, Date, DateTime, Time, Boolean

from ..db.database import Base

class User(Base):
    __tablename__ = "tbl_usuario"

    usu_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    usu_email = Column(String,unique=True, nullable=False)
    usu_senha = Column(String, nullable=False)
    fcm_token = Column(String, nullable=False)

class Profile(Base):
    __tablename__="tbl_perfil"

    per_id = Column(Integer, primary_key=True, autoincrement=True)
    per_nome = Column(String, index=True)
    per_usuId = Column(Integer, index=True)
    per_foto = Column(String, index=True, default="/default.png")

class Time(Base):
    __tablename__ = "tbl_horario"

    hor_id = Column(Integer, primary_key=True, autoincrement=True)
    hor_horario = Column(Time, nullable=False) 
    hor_medicacao = Column(Integer, nullable=False)

class Monitoring(Base):
    __tablename__ = "tbl_monitoramento"

    mon_id = Column(Integer, primary_key=True, autoincrement=True)
    mon_sintomasId = Column(Integer, nullable=False) #CE
    mon_perfilId = Column(Integer, nullable=False) #CE
    mon_dataHorario = Column(DateTime, nullable=False)

class Confirmation(Base):
    __tablename__ = "tbl_confirmacao"

    con_id = Column(Integer, primary_key=True, autoincrement=True)
    con_medicacaoId = Column(Integer, nullable=False) #CE
    con_horarioId = Column(Integer, nullable=False) #CE
    con_dataHorario = Column(DateTime, nullable=False)

class Medication(Base):
    __tablename__ = "tbl_medicacao"

    med_id = Column(Integer, primary_key=True, autoincrement=True)
    med_nome = Column(String, nullable=False) 
    med_descricao = Column(String, nullable=False)
    med_tipo = Column(String, nullable=False)  
    med_quantidade = Column(Integer, nullable=False)
    med_dataInicio = Column(Date, nullable=False) 
    med_dataFinal = Column(Date, nullable=False)
    med_perfilId = Column(Integer, nullable=False) #CE
    med_estado = Column(Boolean, nullable=False)

class Symptoms(Base):
    __tablename__ = "tbl_sintomas"

    sin_id = Column(Integer, primary_key=True, autoincrement=True)
    sin_nome = Column(String, nullable=False) 

