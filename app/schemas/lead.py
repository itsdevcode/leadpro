from pydantic import BaseModel, ConfigDict, EmailStr
from app.enum.lead import LeadStatus,LeadPriority
from datetime import datetime
from typing import ClassVar

class LeadBase(BaseModel):
    user_id:int
    title: str
    notes: str | None = None
    name: str
    phone: str
    email: EmailStr | None = None
    status: LeadStatus = LeadStatus.NEW
    priority: LeadPriority | None = None
    lead_source: str | None
    next_follow_up: datetime | None = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    title: str | None = None
    notes: str | None = None
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    status: LeadStatus | None = None
    priority: LeadPriority | None = None
    lead_source: str | None = None
    next_follow_up: datetime | None = None

class LeadInDb(LeadBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

class LeadResponse(LeadInDb):
    pass

class LeadListResponse(BaseModel):
    leads: list[LeadResponse]
    page: int
    size: int
    total: int