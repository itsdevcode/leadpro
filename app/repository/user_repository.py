from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.user import UserCreate, UserInDb
from app.models.user import User

def create_user(db: Session, user: UserCreate) -> UserInDb:
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

def get_user_by_email(db: Session, email: str) -> UserInDb | None:
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
    