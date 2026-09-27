from app.schemas.lead import LeadCreate, LeadUpdate
from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.models.user import User
from datetime import datetime

def get_lead_by_id(db: Session, id: int) -> Lead | None:
    return db.query(Lead).filter(Lead.id == id).first()

def create_lead(db: Session, lead: LeadCreate, user: User):
    new_lead = Lead(
        user_id=user.id,
        title=lead.title,
        notes=lead.notes,
        name=lead.name,
        phone=lead.phone,
        email=lead.email,
        status=lead.status,
        priority=lead.priority,
        lead_source=lead.lead_source,
        next_follow_up=lead.next_follow_up
    )
    db.add(new_lead)
    return new_lead

def update_lead(db: Session, lead: LeadUpdate, user: User, id: int) -> Lead | None:
    lead_obj = get_lead_by_id(db, id)
    if not lead_obj:
        raise Exception("Lead not found")
    updated_lead = lead.model_dump(exclude_unset=True)
    for key, value in updated_lead.items():
        setattr(lead_obj, key, value)
    lead_obj.updated_at = datetime.now()
    return lead_obj

def delete_lead(db: Session, user: User, id: int):
    lead_obj = get_lead_by_id(db, id)
    if not lead_obj:
        raise Exception("Lead not found")
    db.delete(lead_obj)
    return lead_obj

def get_lead_list(db: Session, user: User, page: int, size: int) -> list[Lead]:
    return db.query(Lead).filter(Lead.user_id == user.id).offset((page - 1) * size).limit(size).all()


def get_lead_count(db: Session, user: User) -> int:
    return db.query(Lead).filter(Lead.user_id == user.id).count()
