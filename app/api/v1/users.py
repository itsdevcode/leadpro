from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dto.token import TokenResult
from app.models.user import User
from app.schemas.user import UserCreate, UserInDb, UserLogin,LoginResponse
from app.schemas.otp import OtpVerify
from app.schemas.token import TokenResponse, RefreshTokenRequest
from app.core.database import get_db
import app.services.user_service as user_service
from app.exceptions.user_exceptions import UserAlreadyExistsException, UserNotFoundException
from app.exceptions.otp_exceptions import InvalidOtpException, InvalidRefreshTokenException
from fastapi import Request
from typing import Annotated

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(user: UserLogin, db: Annotated[Session, Depends(get_db)]) ->LoginResponse:
    try:
        result = user_service.login(db, user)
        return LoginResponse(
            message=result.message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.post("/", response_model=UserInDb)
def create_user(
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """
    Creates a new user.
    
    Args:
        user: The user data to create.
        db: The database session.
    
    Returns:
        The created user.
    """
    try:
        user_obj = user_service.create_user(db, user)
        return user_obj
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.post("/otp/verify", response_model=TokenResponse)
def verify_otp(
    otp: OtpVerify,
    request: Request,
    db: Annotated[Session, Depends(get_db)]
) -> TokenResponse:
    try:
        result: TokenResult = user_service.verify_otp(db, otp, request)
        return TokenResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
            expires_in=result.expires_in,
        )

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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {e}",
        )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    payload: RefreshTokenRequest,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    try:
        result: TokenResult = user_service.refresh_access_token(
            db=db,
            raw_refresh_token=payload.refresh_token,
            user_agent=request.headers.get("user-agent"),
            ip_address=request.client.host if request.client else None, 
        )
        return TokenResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
            expires_in=result.expires_in,
        )
    except InvalidRefreshTokenException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")    