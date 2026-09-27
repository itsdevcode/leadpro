from app.dto.lead import LeadListResult
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadListResponse, LeadUpdate
from sqlalchemy.orm import Session
import app.repository.lead_repository as lead_repository
from app.models.user import User

def create_lead(db: Session, lead: LeadCreate, user: User):
    try:
        lead_data = lead_repository.create_lead(db, lead, user)
        db.commit()
        db.refresh(lead_data)
        return lead_data
    except Exception as e:
        db.rollback()
        raise e

def update_lead(db: Session, lead: LeadUpdate, user: User, id: int):
    try:
        lead_data = lead_repository.update_lead(db, lead, user, id)
        db.commit()
        db.refresh(lead_data)
        return lead_data
    except Exception as e:
        db.rollback()
        raise e

def delete_lead(db: Session, user: User, id: int):
    try:
        lead_data = lead_repository.delete_lead(db, user, id)
        db.commit()
        return lead_data
    except Exception as e:
        db.rollback()
        raise e

def leads_list(db: Session, user: User, page: int, size: int) ->LeadListResult:
    try:
        lead_data = lead_repository.get_lead_list(db, user, page, size)
        total = lead_repository.get_lead_count(db, user)
        return LeadListResult(
            leads=lead_data,
            page=page,
            size=size,
            total=total
        )
    except Exception as e:
        raise e