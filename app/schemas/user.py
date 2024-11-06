from uuid import UUID

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Union
from app.models.user import UserRole


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    first_name: str | None = None
    last_name: str | None = None
    role: UserRole = UserRole.client


class UserLogin(UserBase):
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class User(UserBase):
    id: UUID
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    is_active: bool
    role: UserRole or None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True


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


# Client profile response model
class ClientProfileResponse(BaseModel):
    id: UUID
    country: Optional[str]
    # orders: Optional[int]
    accepted_orders: Optional[int]
    pay_rate: Optional[float]
    balance: Optional[float]

    class Config:
        from_attributes = True
        orm_mode = True


# Writer profile response model
class WriterProfileResponse(BaseModel):
    id: UUID
    reviews: Optional[str]
    orders: Optional[int]
    success_rate: Optional[float]
    about_me: Optional[str]
    status: Optional[str]
    profile_picture: Optional[str]
    skills: Optional[List[str]]
    languages: Optional[List[str]]

    class Config:
        from_attributes = True
        orm_mode = True


# Combined response model for user with optional profile
class UserWithProfileResponse(BaseModel):
    user: User
    profile: Optional[Union[ClientProfileResponse, WriterProfileResponse]] = None

    class Config:
        orm_mode = True
