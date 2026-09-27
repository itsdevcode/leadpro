from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.schemas.lead import LeadCreate, LeadListResponse, LeadResponse, LeadUpdate
from sqlalchemy.orm import Session
from app.core.database import get_db
import app.services.lead_service as lead_service
from app.utils.auth import current_user


router = APIRouter()

@router.post("/create")
def create_lead(lead: LeadCreate, current_user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]):
    try:
        return lead_service.create_lead(db, lead, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.patch("/{id}")
def update_lead(id: int, lead: LeadUpdate, current_user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]):
    try:
        return lead_service.update_lead(db, lead, current_user, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.delete("/{id}")
def delete_lead(id: int, current_user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]):
    try:
        return lead_service.delete_lead(db, current_user, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.get("/", response_model=LeadListResponse)
def leads_list(current_user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)], page: int = 1, size: int = 10) -> LeadListResponse:
    try:
        result = lead_service.leads_list(db, current_user, page, size)
        leads_list_response = LeadListResponse(
           leads=[
               LeadResponse.model_validate(lead)
               for lead in result.leads
           ],
            page=result.page,
            size=result.size,
            total=result.total
        )
        return leads_list_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
