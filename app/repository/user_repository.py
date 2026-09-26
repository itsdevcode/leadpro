from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.schemas.user import UserCreate, UserInDb
from app.schemas.otp import OtpCreate
from app.models.user import User
from app.models.otp import Otp
from app.models.refresh_tokens import RefreshToken
from app.utils.jwt import hash_token
from datetime import datetime

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

def create_otp(db: Session, otp: OtpCreate) -> Otp:
    """
    Create or update an OTP for a user atomically.
    
    Args:
        db: Database session.
        otp: OTP data.
    
    Returns:
        Created or updated OTP.
    """
    stmt = (
        insert(Otp)
        .values(
            user_id=otp.user_id,
            code=otp.otp_code,
            expires_at=otp.expires_at,
            is_used=otp.is_used,
            created_at=datetime.now(),
        )
        .on_conflict_do_update(
            index_elements=[Otp.user_id],
            set_={
                "code": otp.otp_code,
                "expires_at": otp.expires_at,
                "is_used": otp.is_used,
                "updated_at": datetime.now(),
            },
        )
        .returning(Otp)
    )
    return db.execute(stmt).scalar_one()

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
    
def get_otp_by_user_id(db: Session, user_id: int) -> Otp | None:
    stmt = select(Otp).where(Otp.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()

def save_refresh_token(db: Session, user_id: int, token: str, expires_at: datetime, user_agent: str | None, ip_address: str | None):
    db_refresh_token = RefreshToken(
        user_id=user_id,
        token_hash=hash_token(token),
        expires_at=expires_at,
        user_agent=user_agent,
        ip_address=ip_address
    )
    db.add(db_refresh_token)
    return db_refresh_token

def verify_refresh_token(db: Session, token_hash: str) -> RefreshToken | None:
    stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    return db.execute(stmt).scalar_one_or_none()
