from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserInDb
from app.schemas.otp import OtpVerify
from app.core.database import get_db
import app.services.user_service as user_service
from app.exceptions.user_exceptions import UserAlreadyExistsException, UserNotFoundException
from app.exceptions.otp_exceptions import InvalidOtpException

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
    
@router.post("/otp/verify", response_model=UserInDb)
def verify_otp(
    otp: OtpVerify,
    db: Session = Depends(get_db),
) -> UserInDb:
    try:
        return user_service.verify_otp(db, otp)

    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except InvalidOtpException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )
    