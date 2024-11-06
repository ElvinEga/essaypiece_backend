from enum import Enum

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderStatus(str, Enum):
    draft = "draft"
    open = "open"
    closed = "closed"
    cancelled = "cancelled"


class Space(str, Enum):
    double = "double"
    single = "single"


class SizeType(str, Enum):
    pages = "pages"
    words = "words"


class Language(int, Enum):
    english_us = 0
    english_uk = 1
    spanish_es = 2
    french_fr = 3


class Service(int, Enum):
    writing = 0
    rewriting = 1
    editing = 2
    proofreading = 3
    problem_solving = 4
    calculations = 5


class CitationStyle(int, Enum):
    APA_6th = 0
    APA_7th = 1
    ASA = 2
    Bluebook = 3
    Chicago_Turabian = 4
    Harvard = 5
    IEEE = 6
    MLA = 7
    Other = 8
    Not_applicable = 9


class Academic(int, Enum):
    high_school = 0
    college = 1
    bachelors = 2
    masters = 3
    doctorate = 4


class OrderBase(BaseModel):
    product: Optional[int]
    deadline: Optional[datetime]
    for_final_date: Optional[datetime]
    language: Optional[int]
    level: Optional[int]
    service: Optional[int]
    quantity: Optional[int]
    space: Optional[int]
    words_count: Optional[int]
    size_type: Optional[str]
    topic: Optional[str]
    description: Optional[str]
    price: Optional[float]
    subject: Optional[str]
    number_of_sources: Optional[int]
    style: Optional[int]
    is_private: Optional[bool]
    promocode: Optional[str]
    client_id: Optional[str]


class OrderCreate(BaseModel):
    product: int
    deadline: datetime
    language: Language
    level: Academic
    service: Service
    quantity: int
    space: str
    words_count: int
    size_type: str
    topic: str
    description: str
    subject: int
    number_of_sources: int
    style: CitationStyle
    is_private: bool
    client_id: str
    status: Optional[OrderStatus] = OrderStatus.draft

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True  # Allows the use of Enums


class OrderUpdate(BaseModel):
    product: Optional[int]
    deadline: Optional[datetime]
    language: Optional[Language]
    level: Optional[Academic]
    service: Optional[Service]
    quantity: Optional[int]
    space: Optional[str]
    words_count: Optional[int]
    size_type: Optional[str]
    topic: Optional[str]
    description: Optional[str]
    subject: Optional[int]
    number_of_sources: Optional[int]
    style: Optional[CitationStyle]
    is_private: Optional[bool]
    client_id: Optional[str]
    status: Optional[OrderStatus]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True  # Allows the use of Enums


class OrderResponse(BaseModel):
    id: int
    product: int
    deadline: datetime
    language: int
    level: int
    service: int
    quantity: int
    space: str
    words_count: int
    size_type: str
    topic: str
    description: str
    subject: int
    number_of_sources: int
    style: int
    is_private: bool
    client_id: str
    status: OrderStatus

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
