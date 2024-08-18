# schemas_profile.py
from pydantic import BaseModel # type: ignore
from datetime import time, datetime

class TimeBase(BaseModel):
    hor_horario: time

# Para uso interno e evitar confusão, renomeamos a classe Pydantic para ProfileInDB
class TimeInDB(TimeBase):
    hor_id: int
    hor_horario: time


    class Config:
        from_attributes = True

class ConfirmationBase(BaseModel):
    con_dataHorario: datetime

class ConfirmationEdit(BaseModel):
    con_medicacaoId:int
    con_horarioId:int
    con_perfilId: int
    
# Para uso interno e evitar confusão, renomeamos a classe Pydantic para ProfileInDB
class ConfirmationInDB(ConfirmationBase):
    con_id: int

    class Config:
        from_attributes = True


