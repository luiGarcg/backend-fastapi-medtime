from fastapi import Header, HTTPException, Depends
from jose import jwt
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
# Função para validar e obter o usuário atual a partir do token JWT
def get_current_user(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
