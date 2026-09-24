import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserInDb
from app.schemas.otp import OtpCreate
from app.repository import user_repository
from app.exceptions.user_exceptions import UserAlreadyExistsException, UserNotFoundException, UserNotActiveException
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
