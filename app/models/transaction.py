from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class TransactionType(enum.Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"


class TransactionStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Add ForeignKey to reference User
    amount = Column(Float, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False, default=TransactionStatus.pending)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)

    # Define relationship to User
    user = relationship("User", back_populates="transactions")
