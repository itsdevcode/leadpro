from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class OtpCreate(BaseModel):
    user_id: int
    otp_code: str
    expires_at: datetime
    is_used: bool = False


class OtpVerify(BaseModel):
    email: EmailStr
    otp_code: str


class OtpInDb(BaseModel):
    id: int
    user_id: int
    otp_code: str
    expires_at: datetime
    is_used: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)