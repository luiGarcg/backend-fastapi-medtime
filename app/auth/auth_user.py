from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..db.models import User, Profile
from ..user.schemas_user import UserBase
from .schemas_auth import AuthSignUp
from ..db.models import User, Profile
from ..user.schemas_user import UserBase
from .schemas_auth import AuthSignUp
from aiocache import cached, Cache
from app.config import cache


class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def is_email_registered(self, email: str) -> bool:
        return self.db_session.query(User).filter(User.usu_email == email).first() is not None

    def user_register(self, user: AuthSignUp):
        # Verifica se o email já está registrado
        if self.is_email_registered(user.usu_email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already registered'
            )

        user_model = User(
            usu_email=user.usu_email,
            usu_senha=self.crypt_context.hash(user.usu_senha)
        )

        try:
            self.db_session.add(user_model)
            self.db_session.commit()
            self.db_session.refresh(user_model)

            profile_model = Profile(
                per_nome=user.per_nome,
                per_usuId=user_model.usu_id
            )
            self.db_session.add(profile_model)
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )
        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Internal server error'
            ) from e

    async def user_login(self, user: UserBase) -> dict:
        user_on_db = self.db_session.query(User).filter_by(usu_email=user.usu_email).first()

        if user_on_db is None or not self.crypt_context.verify(user.usu_senha, user_on_db.usu_senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email or password is invalid'
            )
        
        # Armazena o user_id no cache
        await cache.set("global_user_id", user_on_db.usu_id)

        return {
            'id': user_on_db.usu_id,
            'email': user_on_db.usu_email,
        }