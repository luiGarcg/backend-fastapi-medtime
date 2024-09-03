from pydantic import BaseModel # type: ignore

class SymptomsBase(BaseModel):
    sin_nome: str

class SymptomsInBD(SymptomsBase):
    sin_id: int

    class Config:
        from_attributes = True