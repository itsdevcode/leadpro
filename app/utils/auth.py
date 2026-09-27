from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.database import get_db
from app.models.user import User
from app.utils.jwt import decode_access_token
from app.repository import user_repository
from app.exceptions.user_exceptions import UserNotFoundException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    try:
        payload = decode_access_token(token)
        user_obj = user_repository.get_user_by_id(db, int(payload["sub"]))
        if not user_obj:
            raise UserNotFoundException("User not found")
        return user_obj
    except Exception:
        db.rollback()
        raise