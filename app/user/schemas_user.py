from pydantic import BaseModel, field_validator
import re

#define o que o programa precisa receber para executar a ação
class UserBase(BaseModel):
    usu_email: str
    usu_senha: str

    @field_validator('usu_email')
    def validate_email(cls,value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError('email format is invalid')
        return value
    
#herda de userBase os atributos e é usado para criação de novos usuarios 
class UserCreate(UserBase):
    pass

#herda de userBase os atributo e é usado para buscar dados
class User(UserBase):
    usu_id: int

    class Config:
        orm_mode = True
