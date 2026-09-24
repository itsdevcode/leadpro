from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserInDb
from app.repository import user_repository
from app.exceptions.user_exceptions import UserAlreadyExistsException, UserNotFoundException, UserNotActiveException

def create_user(db: Session, user: UserCreate) -> UserInDb:
    try:
        user_obj = user_repository.get_user_by_email(db, user.email)
        if user_obj:
            raise UserAlreadyExistsException("User with this email already exists")
        user_obj = user_repository.create_user(db, user)
        db.commit()
        db.refresh(user_obj)
        return user_obj
    except UserAlreadyExistsException as e:
        db.rollback()
        raise
