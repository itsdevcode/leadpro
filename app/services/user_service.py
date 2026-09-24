import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.schemas.otp import OtpCreate, OtpVerify
from app.schemas.user import UserCreate, UserInDb
from app.repository import user_repository
from app.exceptions.user_exceptions import UserAlreadyExistsException, UserNotFoundException, UserNotActiveException
from app.exceptions.otp_exceptions import InvalidOtpException
from sqlalchemy.exc import IntegrityError
from app.models.user import User

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

def verify_otp(db: Session, otp: OtpVerify) ->User:
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
        db.commit()
        return user_obj
    except Exception:
        db.rollback()
        raise
    