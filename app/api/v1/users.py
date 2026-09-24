from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserInDb
from app.core.database import get_db
import app.services.user_service as user_service
from app.exceptions.user_exceptions import UserAlreadyExistsException

router = APIRouter()


@router.post("/", response_model=UserInDb | None)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
) -> UserInDb | None:
    """
    Creates a new user.
    
    Args:
        user: The user data to create.
        db: The database session.
    
    Returns:
        The created user.
    """
    try:
        user = user_service.create_user(db, user)
        return user
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
