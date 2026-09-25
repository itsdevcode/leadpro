
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 60 * 60 * 24
    
    model_config = ConfigDict(from_attributes=True)


class TokenPairInDb(BaseModel):
    id: int
    user_id: int
    token_hash: str
    expires_at: datetime
    revoked: bool
    replaced_by_token_id: int | None
    ip_address: str | None
    user_agent: str | None
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str
    