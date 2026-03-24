from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.auth import UserCreate, UserLogin
from core.security import hash_password, verify_password, create_access_token


def register_user(db: Session, data: UserCreate):

    # check duplicate email
    if db.query(UserModel).filter_by(email=data.email).first():
        raise ValueError("Email already taken")

    user = UserModel(
        username=data.username, email=data.email, password=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(db: Session, data: UserLogin):

    user = db.query(UserModel).filter_by(email=data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise ValueError("Invalid email or password")

    token = create_access_token({"sub": str(user.id)})

    return token
