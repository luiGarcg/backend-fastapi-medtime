from sqlalchemy.orm import Session
from . import schemas_profile
from ..db.models import Profile

#faz a busca de dados na tabela tbl_usuario
def get_profile(db: Session, per_id: int):
    return db.query(Profile).filter(Profile.per_id == per_id).first()

#adiciona novos dados na tabela tbl_usuario
def create_profile(db: Session, profile: schemas_profile.ProfileCreate):
    db_profile = Profile(per_nome=profile.per_nome, per_usuId=profile.per_usuId ,per_foto=profile.per_foto)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile
