from pydantic import BaseModel, field_validator
import re

class AuthSignIn(BaseModel):
    per_nome: str
    usu_email: str
    usu_senha: str

class LoginSchema(BaseModel):
    usu_email: str
    usu_senha: str

    @field_validator('usu_email')
    def validate_email(cls, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError('email format is invalid')
        return value