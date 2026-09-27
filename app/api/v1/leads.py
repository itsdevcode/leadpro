from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.lead import LeadCreate
from sqlalchemy.orm import Session, session
from app.core.database import get_db
import app.services.lead_service as lead_service

router = APIRouter()


@router.get("/")
def leads_list():
    return {
        'hey':"Welcome Task"
    }

@router.post("/create")
def create_lead(lead: LeadCreate, db: Annotated[Session, Depends(get_db)]):
    try:
        return lead_service.create_lead(db, lead)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
