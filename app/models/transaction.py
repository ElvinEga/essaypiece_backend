import uuid

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class TransactionType(enum.Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"


class Sign(enum.Enum):
    positive = "+"
    negative = "-"


class TransactionStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Add ForeignKey to reference User
    sign = Column(Enum(Sign), nullable=False, default=Sign.positive)
    amount = Column(Float, nullable=False)
    transaction_number = Column(String, unique=True, default=lambda: str(uuid.uuid4()))  # Unique transaction number
    transaction_type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False, default=TransactionStatus.pending)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=func.now())  # Timestamp of creation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    # Define relationship to User
    user = relationship("User", back_populates="transactions")


metadata = Base.metadata
