from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class OtpBase(BaseModel):
    phone_number: str
    otp_code: str


class OtpCreate(OtpBase):
    expires_at: datetime


class OtpVerify(OtpBase):
    pass


class OtpInDb(OtpBase):
    id: int
    expires_at: datetime
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
