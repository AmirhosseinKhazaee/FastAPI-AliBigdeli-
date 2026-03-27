from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.auth import UserCreate, UserLogin
from core.security import (
    decode_token,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)


def register_user(db: Session, data: UserCreate):

    if db.query(UserModel).filter(UserModel.email == data.email).first():
        raise ValueError("Email already taken")

    user = UserModel(
        username=data.username,
        email=data.email,
        password=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(db: Session, data: UserLogin):

    user = db.query(UserModel).filter_by(email=data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise ValueError("Invalid email or password")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def refresh_access_token(db: Session, refresh_token: str):

    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh":
        raise ValueError("Invalid refresh token")

    user_id = payload["sub"]

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise ValueError("User no longer exists")

    access_token = create_access_token(user.id)

    return {"access_token": access_token}
