# schemas_profile.py
from pydantic import BaseModel # type: ignore
from datetime import datetime

class ProfileBase(BaseModel):
    per_nome: str

class ProfileUpdateImage(BaseModel):
    per_foto:str
    
# Para uso interno e evitar confusão, renomeamos a classe Pydantic para ProfileInDB
class ProfileInDB(ProfileBase):
    per_id: int

    class Config:
        from_attributes = True

