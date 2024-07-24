# schemas_profile.py
from pydantic import BaseModel
from datetime import time

class TimeBase(BaseModel):
    hor_horario: time

# Para uso interno e evitar confusão, renomeamos a classe Pydantic para ProfileInDB
class TimeInDB(TimeBase):
    hor_id: int
    hor_horario: time


    class Config:
        from_attributes = True
