from pydantic import BaseModel, field_validator
import re

class AuthSignUp(BaseModel):
    per_nome: str
    usu_email: str
    usu_senha: str
    fcm_token: str 

class LoginSchema(BaseModel):
    usu_email: str
    usu_senha: str

    @field_validator('usu_email')
    def validate_email(cls, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError('email format is invalid')
        return value