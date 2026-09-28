from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LeadCommentBase(BaseModel):
    comment: str

class LeadCommentCreate(LeadCommentBase):
    pass

class LeadCommentUpdate(BaseModel):
    comment: str

class LeadCommentResponse(LeadCommentBase):
    id: int
    lead_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class LeadCommentListResponse(BaseModel):
    comments: list[LeadCommentResponse]
    page: int
    size: int
    total: int

    model_config = ConfigDict(from_attributes=True)