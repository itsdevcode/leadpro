from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.lead_comment import LeadCommentCreate, LeadCommentListResponse, LeadCommentResponse, LeadCommentUpdate
from app.services import lead_comment_service
from app.utils.auth import current_user

router = APIRouter()

@router.post("/create/{lead_id}")
def create_lead_comment(lead_id: int,
                        lead_comment: LeadCommentCreate,
                        current_user: Annotated[User, Depends(current_user)],
                        db: Annotated[Session, Depends(get_db)]) -> LeadCommentResponse:
    try:
        comment = lead_comment_service.create_lead_comment(db, lead_id, current_user, lead_comment)
        return comment
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal Server Error {e}")

@router.patch("/{comment_id}")
def update_lead_comment(
    comment_id: int,
    user: Annotated[User, Depends(current_user)],
    lead_comment: LeadCommentUpdate,
    db: Annotated[Session, Depends(get_db)]
) -> LeadCommentResponse:
    try:
        comment = lead_comment_service.update_lead_comment(comment_id, user, lead_comment, db)
        return comment
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Interal Server Error {e}")

@router.delete("/{comment_id}")
def delete_lead_comment(comment_id: int,
    user: Annotated[User, Depends(current_user)],
    db: Annotated[Session, Depends(get_db)]) -> LeadCommentResponse:
    try:
        comment = lead_comment_service.delete_comment(comment_id, user, db)
        return comment
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Interal Server Error {e}")

@router.get("/")
def comment_list(user: Annotated[User, Depends(current_user)], 
                   db: Annotated[Session, Depends(get_db)], 
                   page: int = 1, 
                   size: int = 10) -> LeadCommentListResponse:
    try:
        comments = lead_comment_service.get_comment_list(db, user, page, size)
        return comments
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Interal Server Error {e}")