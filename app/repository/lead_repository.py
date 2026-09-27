from app.schemas.lead import LeadCreate
from sqlalchemy.orm import Session
from app.models.lead import Lead

def create_lead(db: Session, lead: LeadCreate):
    new_lead = Lead(
        user_id=lead.user_id,
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