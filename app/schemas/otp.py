from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class OtpBase(BaseModel):
    user_id: int
    otp_code: str
    expires_at: datetime
    is_used: bool


class OtpCreate(OtpBase):
    pass


class OtpVerify(OtpBase):
    pass


class OtpInDb(OtpBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
