from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"


class Sign(str, Enum):
    positive = "+"
    negative = "-"


class TransactionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class TransactionBase(BaseModel):
    amount: float
    transaction_type: TransactionType
    transaction_number: str
    sign: Sign = Sign.positive
    payment_method: Optional[str]
    status: Optional[str]
    description: Optional[str]


class TransactionCreate(TransactionBase):
    user_id: int


class TransactionUpdate(TransactionBase):
    pass


class TransactionOut(TransactionBase):
    id: int
    transaction_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Schema for creating or updating transactions
# class TransactionCreate(BaseModel):
#     amount: float
#     transaction_type: TransactionType
#     description: Optional[str]


class TransactionRead(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: TransactionType
    status: TransactionStatus
    description: Optional[str]
    date: datetime

    class Config:
        orm_mode = True
