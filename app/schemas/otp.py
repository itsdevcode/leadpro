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
