from fastapi import APIRouter, Depends, HTTPException ,status
from sqlalchemy.orm import Session
from core.deps import get_current_user
from models.user import UserModel
from core.database import get_db
from schemas.auth import UserCreate, UserLogin, Token, RefreshTokenRequest, AccessToken
from services.auth import register_user, login_user, refresh_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=Token)
def register(data: UserCreate, db: Session = Depends(get_db)):
    try:
        register_user(db, data)
        return login_user(db, UserLogin(email=data.email, password=data.password))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        return login_user(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/refresh", response_model=AccessToken)
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        return refresh_access_token(db, data.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me")
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user
