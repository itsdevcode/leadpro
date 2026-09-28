
from sqlalchemy.orm import Session
from app.models.user import User
from app.repository import lead_comment_repository
from app.schemas.lead_comment import LeadCommentCreate, LeadCommentListResponse, LeadCommentResponse, LeadCommentUpdate


def create_lead_comment(db: Session, lead_id: int, user: User, lead_comment: LeadCommentCreate) -> LeadCommentResponse:
    try:
        comment = lead_comment_repository.create_comment(db,  user, lead_id, lead_comment)
        db.commit()
        db.refresh(comment)
        return LeadCommentResponse.model_validate(comment)
    except Exception:
        db.rollback()
        raise

def update_lead_comment(comment_id: int, user: User, lead_comment: LeadCommentUpdate, db: Session) -> LeadCommentResponse:
    try:
        comment = lead_comment_repository.update_comment(comment_id, user, lead_comment, db)
        db.commit()
        db.refresh(comment)
        return LeadCommentResponse.model_validate(comment)
    except Exception:
        db.rollback()
        raise

def delete_comment(comment_id: int, user: User, db: Session)-> LeadCommentResponse:
    try:
        comment = lead_comment_repository.delete_comment(db, user, comment_id)
        db.commit()
        return LeadCommentResponse.model_validate(comment)
    except Exception:
        db.rollback()
        raise

def get_comment_list(db: Session, user: User, page: int, size: int) -> LeadCommentListResponse:
    try:
        comments = lead_comment_repository.get_comment_list(db, user, page, size)
        comments_list = [LeadCommentResponse.model_validate(comment) for comment in comments]
        total = lead_comment_repository.get_comment_count(db, user)
        return LeadCommentListResponse(comments=comments_list, page=page, size=size, total=total)
    except Exception:
        raise