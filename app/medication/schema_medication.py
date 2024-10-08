# schemas_profile.py
from pydantic import BaseModel
from datetime import date,time
from typing import List


class MedicationReturn(BaseModel):
    med_nome: str
    med_descricao: str
    med_tipo: str 
    med_quantidade: int
    med_dataInicio: date 
    med_dataFinal: date 
    hor_horario: List[time]  
      
class MedicationBase(BaseModel):
    med_nome: str
    med_descricao: str
    med_tipo: str 
    med_quantidade: int
    med_dataInicio: date 
    med_dataFinal: date 
    med_estado: bool

class MedicationEdit(MedicationBase):
    med_perfilId: int

class MedicationInDB(MedicationBase):
    med_id: int

    class Config:
        from_attributes = True
