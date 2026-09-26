import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.schemas.otp import OtpCreate, OtpVerify
from app.schemas.user import UserCreate, UserInDb, UserLogin, LoginResponse
from app.schemas.token import TokenResponse
from app.repository import user_repository
from app.exceptions.user_exceptions import UserAlreadyExistsException, UserNotFoundException, UserNotActiveException
from app.exceptions.otp_exceptions import InvalidOtpException,InvalidRefreshTokenException
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.core.config import settings
from fastapi import Request
from app.utils.jwt import create_access_token, create_refresh_token, hash_token

def create_user(db: Session, user: UserCreate) -> User:
    try:
        user_obj = user_repository.get_user_by_email(db, user.email)
        if user_obj:
            raise UserAlreadyExistsException("User with this email already exists")
        user_obj = user_repository.create_user(db, user)
        db.flush()
        otp = secrets.randbelow(900000) + 100000
        otp_obj = user_repository.create_otp(db, OtpCreate(
            user_id=user_obj.id,
            otp_code=str(otp),
            expires_at=datetime.now() + timedelta(minutes=10),
            is_used=False
        ))
        db.commit()
        db.refresh(user_obj)
        return user_obj

    except UserAlreadyExistsException as e:
        db.rollback()
        raise

    except IntegrityError:
        db.rollback()
        raise UserAlreadyExistsException(
            "User with this email already exists"
        )

    except Exception:
        db.rollback()
        raise

def verify_otp(db: Session, otp: OtpVerify, request: Request) ->TokenResponse:
    try:
        user_obj = user_repository.get_user_by_email(db, otp.email)
        if not user_obj:
            raise UserNotFoundException("User not found")
     
        otp_obj = user_repository.get_otp_by_user_id(db, user_obj.id)
        if not otp_obj:
            raise InvalidOtpException("Invalid OTP")

        if otp_obj.is_used:
            raise InvalidOtpException("Invalid OTP")

        if otp_obj.expires_at <= datetime.now():
            raise InvalidOtpException("Invalid OTP")

        if otp_obj.code != otp.otp_code:
            raise InvalidOtpException("Invalid OTP")
        
        otp_obj.is_used = True
        access_token = create_access_token(str(user_obj.id))
        refresh_token = create_refresh_token()
        expires_at = datetime.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        user_agent = request.headers.get("User-Agent")
        ip_address = request.client.host
        
        db_refresh_token = user_repository.save_refresh_token(db, user_obj.id, refresh_token, expires_at, user_agent, ip_address)        
        db.commit()
        db.refresh(db_refresh_token)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }
    except Exception:
        db.rollback()
        raise
    
def refresh_access_token(db: Session, raw_refresh_token: str, user_agent: str | None, ip_address: str | None) -> TokenResponse:
    token_hash = hash_token(raw_refresh_token)
    db_token = user_repository.verify_refresh_token(db, token_hash)

    if not db_token:
        raise InvalidRefreshTokenException("Invalid refresh token")

    if db_token.revoked:
        raise InvalidRefreshTokenException("Token reuse detected, all sessions revoked")

    if db_token.expires_at < datetime.now():
        raise InvalidRefreshTokenException("Refresh token expired")
        
    db_token.revoked = True
    new_raw_refresh_token = create_refresh_token()
    expires_at = datetime.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    db_refresh_token = user_repository.save_refresh_token(db, db_token.user_id, new_raw_refresh_token, expires_at, user_agent, ip_address)
    db.flush()
    db_token.replaced_by_token_id = db_refresh_token.id
    db.commit()
    new_access_token = create_access_token(str(db_token.user_id))
    return {
        "access_token": new_access_token,
        "refresh_token": new_raw_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }   
   
def login(db: Session, user: UserLogin) ->LoginResponse:
    try:
        user_obj = user_repository.get_user_by_email(db, user.email)
        if not user_obj:
            raise UserNotFoundException("User not found")
        if user_obj.is_deleted:
            raise UserNotFoundException("User not found")
        if not user_obj.is_active:
            raise UserNotActiveException("User is not active")
        otp_code = secrets.randbelow(900000) + 100000
        otp_obj = user_repository.create_otp(db, OtpCreate(
            user_id=user_obj.id,
            otp_code=str(otp_code),
            expires_at=datetime.now() + timedelta(minutes=10),
            is_used=False
        ))
        db.commit()
        db.refresh(otp_obj)
        return {
            "message": "OTP sent successfully"
        }
    except Exception:
        db.rollback()
        raise