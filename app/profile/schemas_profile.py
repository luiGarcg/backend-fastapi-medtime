from pydantic import BaseModel

class ProfileBase(BaseModel):
    per_nome: str
    per_usuId: int
    per_foto: str

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    per_id: int

    class Config:
        from_attributes = True
