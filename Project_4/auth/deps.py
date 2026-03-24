import jwt
from core.database import get_db
from models.user import UserModel
from sqlalchemy.orm import Session
from auth.security import decode_token
from fastapi.security import HTTPBearer
from fastapi import Depends , HTTPException ,status


httpbearer_scheme = HTTPBearer()


def get_current_user(token : str = Depends(httpbearer_scheme), db :Session = Depends(get_db)):
    try :
        payload = decode_token(token.credentials)
        user_id = payload.get("sub")
        