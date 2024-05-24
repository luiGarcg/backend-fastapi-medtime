from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import status
from sqlalchemy.orm import Session
from ..user import schemas_user
from ..db.models import User
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['sha256_crypt'])

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def user_register(self, user: schemas_user):
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
        
