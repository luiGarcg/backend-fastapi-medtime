from pydantic import BaseModel

class AuthSignIn(BaseModel):
    per_nome: str
    usu_email: str
    usu_senha: str
