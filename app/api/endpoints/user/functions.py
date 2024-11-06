from fastapi import HTTPException, status, Depends
from typing import Annotated, Union
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

# from auth import models, schemas
from passlib.context import CryptContext
from jose import JWTError, jwt

# import 
from app.models import user as UserModel
from app.schemas.user import UserCreate, UserUpdate, Token, ClientProfileResponse, WriterProfileResponse, \
    UserWithProfileResponse
from app.core.settings import SECRET_KEY, REFRESH_SECRET_KEY, ALGORITHM
from app.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.dependencies import get_db, oauth2_scheme
from app.schemas.user import WriterProfileCreate, ClientProfileCreate, User as UserSchema
from app.models.user import Writer, Client, User, UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(UserModel.User).filter(UserModel.User.email == email).first()


# get user by id
def get_user_by_id(db: Session, user_id: int):
    db_user = db.query(UserModel.User).filter(UserModel.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# crete new user
def create_new_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    new_user = UserModel.User(email=user.email, password=hashed_password, first_name=user.first_name,
                              last_name=user.last_name, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if new_user.role == UserRole.client:
        client_profile = Client(
            id=new_user.id,  # Use the same UUID as the user ID
            user=new_user,
            country=None,  # Set default values or modify based on user input
            accepted_orders=0,
            pay_rate=0.0,
            balance=0.0
        )
        db.add(client_profile)
        db.commit()
        db.refresh(client_profile)

    return new_user


# get all user 
def read_all_user(db: Session, skip: int, limit: int):
    return db.query(UserModel.User).offset(skip).limit(limit).all()


# update user
def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    updated_data = user.model_dump(exclude_unset=True)  # partial update
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# delete user
def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()
    # db.refresh(db_user)
    return {"msg": f"{db_user.email} deleted successfully"}


# =====================> login/logout <============================
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, user: UserCreate):
    member = get_user_by_email(db, user.email)
    if not member:
        return False
    if not verify_password(user.password, member.password):
        return False
    return member


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def refresh_access_token(db: Session, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        # member = await User.get(user_id)
        member = get_user_by_id(db, user_id)
        if member is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"id": member.id, "email": member.email, "role": member.role},
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


# get current users info 

def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)]
) -> UserWithProfileResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        current_email: str = payload.get("email")

        if current_email is None:
            raise credentials_exception

        # Retrieve user by email
        user = get_user_by_email(db, current_email)
        if user is None:
            raise credentials_exception

        # Convert User SQLAlchemy model to Pydantic model
        user_data = UserSchema.from_orm(user)

        # Check and include profile based on user role
        if user.role == UserRole.client:
            client_profile = db.query(Client).filter(Client.id == user.id).first()
            if client_profile:
                profile_data = ClientProfileResponse.from_orm(client_profile)
                return UserWithProfileResponse(user=user_data, profile=profile_data)

        elif user.role == UserRole.writer:
            writer_profile = db.query(Writer).filter(Writer.id == user.id).first()
            if writer_profile:
                profile_data = WriterProfileResponse.from_orm(writer_profile)
                return UserWithProfileResponse(user=user_data, profile=profile_data)

        # For admin or users with no profile, just return the user without profile
        return UserWithProfileResponse(user=user_data, profile=None)

    except JWTError:
        raise credentials_exception


def create_writer_profile(profile: WriterProfileCreate, db: Session):
    writer = Writer(**profile.dict())
    db.add(writer)
    db.commit()
    db.refresh(writer)
    return writer


def create_client_profile(profile: ClientProfileCreate, db: Session):
    client = Client(**profile.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


# Update writer profile
def update_writer_profile(writer_id: int, profile: WriterProfileCreate, db: Session):
    db_writer = db.query(Writer).filter(Writer.id == writer_id).first()
    if not db_writer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Writer not found")

    for key, value in profile.dict(exclude_unset=True).items():
        setattr(db_writer, key, value)

    db.commit()
    db.refresh(db_writer)
    return db_writer


# Delete writer profile
def delete_writer_profile(writer_id: int, db: Session):
    db_writer = db.query(Writer).filter(Writer.id == writer_id).first()
    if not db_writer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Writer not found")

    db.delete(db_writer)
    db.commit()
    return {"detail": "Writer profile deleted"}


# Update client profile
def update_client_profile(client_id: int, profile: ClientProfileCreate, db: Session):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    for key, value in profile.dict(exclude_unset=True).items():
        setattr(db_client, key, value)

    db.commit()
    db.refresh(db_client)
    return db_client


# Delete client profile
def delete_client_profile(client_id: int, db: Session):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    db.delete(db_client)
    db.commit()
    return {"detail": "Client profile deleted"}
