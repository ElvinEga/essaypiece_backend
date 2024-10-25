import enum

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.schemas.order import Service, Language


class OrderStatus(enum.Enum):
    draft = "draft"
    open = "open"
    closed = "closed"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product = Column(Integer, nullable=False)
    deadline = Column(DateTime, nullable=False)
    for_final_date = Column(DateTime, nullable=True)
    language = Column(Enum(Language))
    level = Column(Integer, nullable=False)
    service = Column(Enum(Service))
    quantity = Column(Integer, nullable=False)
    space = Column(Integer, nullable=False)
    words_count = Column(Integer, nullable=False)
    size_type = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    subject = Column(String, nullable=False)
    number_of_sources = Column(Integer, nullable=False)
    style = Column(Integer, nullable=False)
    is_private = Column(Boolean, default=False)
    promocode = Column(String, nullable=True)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="orders")
    status = Column(Enum(OrderStatus), default=OrderStatus.draft, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)