from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.user import UserCreate, UserInDb
from app.schemas.otp import OtpCreate, OtpInDb
from app.models.user import User
from app.models.otp import Otp

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        db: Database session.
        user: User data to create.
    
    Returns:
        Created user.
    """
    db_user = User(
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        is_active=True,
        is_deleted=False
    )
    db.add(db_user)
    return db_user

def create_otp(db: Session, otp:OtpCreate) -> Otp:
    """
    Create a new OTP.
    
    Args:
        db: Database session.
        user_id: User ID.
        code: OTP code.
    
    Returns:
        Created OTP.
    """
    db_otp = Otp(
        user_id=otp.user_id,
        code=otp.otp_code,
        expires_at=otp.expires_at,
        is_used=otp.is_used
    )
    db.add(db_otp)
    return db_otp

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Get user by email.
    
    Args:
        db: Database session.
        email: User email.
    
    Returns:
        User if found, None otherwise.
    """
    return db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()
    