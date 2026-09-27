from typing import ClassVar

from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str | None = None
    is_active: bool = True
    is_deleted: bool = False


class UserLogin(BaseModel):
    email: EmailStr

class LoginResponse(BaseModel):
    message: str

class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    is_active: bool | None = None
    is_deleted: bool | None = None


class UserInDb(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)