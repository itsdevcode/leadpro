from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings
import secrets
import hashlib

from app.exceptions.otp_exceptions import InvalidAccessTokenException


def create_access_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token() -> str:
    return secrets.token_urlsafe(32)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def decode_access_token(token: str) -> dict[str, str]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            raise InvalidAccessTokenException("Invalid token type")
        return payload
    except Exception:
        raise InvalidAccessTokenException("Invalid access token")
        