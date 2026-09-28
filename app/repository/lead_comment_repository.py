from datetime import datetime

from sqlalchemy.orm import Session
from app.models.lead_comments import LeadComment
from app.models.user import User
from app.schemas.lead_comment import LeadCommentCreate, LeadCommentUpdate


def create_comment(db: Session, user: User, lead_id: int, lead_comment: LeadCommentCreate) -> LeadComment:
    new_comment = LeadComment(lead_id=lead_id, user_id=user.id, comment=lead_comment.comment)
    db.add(new_comment)
    return new_comment

def update_comment(comment_id: int, user: User, lead_comment: LeadCommentUpdate, db: Session) -> LeadComment | None:
    try:
        comment_obj = db.query(LeadComment).filter(LeadComment.id == comment_id, LeadComment.user_id == user.id).first()
        if not comment_obj:
            raise Exception("Lead comment not found")
        updated_comment = lead_comment.model_dump(exclude_unset=True)
        for key, value in updated_comment.items():
            setattr(comment_obj, key, value)
        comment_obj.updated_at = datetime.now()
        return comment_obj
    except Exception:
        pass

def delete_comment(db: Session, user: User, comment_id: int) -> LeadComment | None:
    try:
        comment_obj = db.query(LeadComment).filter(LeadComment.id == comment_id, LeadComment.user_id == user.id).first()
        if not comment_obj:
            raise Exception("Lead comment not found")
        db.delete(comment_obj)
        return comment_obj
    except Exception:
        raise

def get_comment_list(db: Session, user: User, page: int, size: int) -> list[LeadComment]:
    try:
        comments = db.query(LeadComment).filter(LeadComment.user_id == user.id).offset((page - 1) * size).limit(size).all()
        return comments
    except Exception:
        raise

def get_comment_count(db: Session, user: User) -> int:
    return db.query(LeadComment).filter(LeadComment.user_id == user.id).count()