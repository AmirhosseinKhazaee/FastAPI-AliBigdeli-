from sqlalchemy.orm import Session
from models.user import UserModel


def is_user_exists(db: Session, email) -> bool:
    term = db.query(UserModel).filter_by(email=email).first()
    return term
