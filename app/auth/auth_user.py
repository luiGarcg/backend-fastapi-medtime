from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from fastapi import status
from sqlalchemy.orm import Session
from ..db.models import User
from ..user.schemas_user import UserBase
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from decouple import config

SECRET_KEY=config('SECRET_KEY')
ALGORITHM=config('ALGORITHM')
crypt_context = CryptContext(schemes=['sha256_crypt'])

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def user_register(self, user: UserBase):
        user_model = User(
            usu_email= user.usu_email,
            usu_senha= crypt_context.hash(user.usu_senha)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )
        
    def user_login(self, user: UserBase, expires_in: int = 30):
        user_on_db = self.db_session.query(User).filter_by(usu_email=user.usu_email).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='email or password is invalid'
            )
        if not crypt_context.verify(user.usu_senha, user_on_db.usu_senha):  # Corrigido para verificar a senha
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='email or password is invalid'
            )

        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in)

        payload = {
            'sub': user.usu_email,
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }
