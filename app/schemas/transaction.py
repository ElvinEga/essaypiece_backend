from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"


class TransactionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


# Schema for creating or updating transactions
class TransactionCreate(BaseModel):
    amount: float
    transaction_type: TransactionType
    description: Optional[str]


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
