from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
import jwt
from sqlalchemy.orm import Session
from core.security import decode_token
from core.database import get_db
from models.user import UserModel

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
httpbearer_scheme = HTTPBearer()


def get_current_user(
    token: str = Depends(httpbearer_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_token(token.credentials)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
