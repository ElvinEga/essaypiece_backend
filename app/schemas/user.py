from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.user import UserRole


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    first_name: str | None = None
    last_name: str | None = None


class UserLogin(UserBase):
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class User(UserBase):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    is_active: bool
    role: UserRole or None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None
    role: UserRole or None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class WriterProfileCreate(BaseModel):
    reviews: Optional[str]
    orders: Optional[int]
    success_rate: Optional[float]
    about_me: Optional[str]
    status: Optional[str]
    profile_picture: Optional[str]
    skills: Optional[List[str]]
    languages: Optional[List[str]]


# Client profile schema for creating or updating
class ClientProfileCreate(BaseModel):
    country: Optional[str]
    orders: Optional[int]
    accepted_orders: Optional[int]
    pay_rate: Optional[float]
    balance: Optional[float]
