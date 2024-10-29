from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey, Enum
from enum import Enum as PythonEnum

from sqlalchemy.orm import relationship

from app.core.database import Base
from .common import CommonModel


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Language(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


# Skills and Languages tables (many-to-many)
writer_skills = Table(
    'writer_skills', Base.metadata,
    Column('writer_id', Integer, ForeignKey('writers.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

writer_languages = Table(
    'writer_languages', Base.metadata,
    Column('writer_id', Integer, ForeignKey('writers.id')),
    Column('language_id', Integer, ForeignKey('languages.id'))
)


class UserRole(PythonEnum):
    client = "client"
    admin = "admin"
    writer = "writer"


class User(CommonModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, unique=True)
    role = Column(Enum(UserRole), default=UserRole.client)
    transactions = relationship("Transaction", back_populates="user")

    def __repr__(self):
        return f"{self.email}"


class Writer(Base):
    __tablename__ = 'writers'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("User")
    reviews = Column(String)
    orders = Column(Integer)
    success_rate = Column(Float)
    about_me = Column(String)
    status = Column(String)
    profile_picture = Column(String)
    skills = relationship("Skill", secondary=writer_skills)
    languages = relationship("Language", secondary=writer_languages)


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("User")
    country = Column(String)
    orders = relationship("Order", back_populates="client")
    accepted_orders = Column(Integer)
    pay_rate = Column(Float)
    balance = Column(Float)


metadata = Base.metadata
