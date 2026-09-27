from app.schemas.lead import LeadCreate
from sqlalchemy.orm import Session
import app.repository.lead_repository as lead_repository

def create_lead(db: Session, lead: LeadCreate):
    try:
        lead_data = lead_repository.create_lead(db, lead)
        db.commit()
        db.refresh(lead_data)
        return lead_data
    except Exception as e:
        db.rollback()
        raise e
