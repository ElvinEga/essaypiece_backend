# fastapi 
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from datetime import timedelta
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
import os

# sqlalchemy
from sqlalchemy.orm import Session

# import
from app.schemas.user import User, UserLogin, Token, RefreshTokenRequest
from app.core.dependencies import get_db
from app.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.api.endpoints.user import functions as user_functions

auth_module = APIRouter()

config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'openid email profile'},
)


# ============> login/logout < ======================
# getting access token for login 
@auth_module.post("/login", response_model=Token)
async def login_for_access_token(
        user: UserLogin,
        db: Session = Depends(get_db)
) -> Token:
    member = user_functions.authenticate_user(db, user=user)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_functions.create_access_token(
        data={"id": member.id, "email": member.email, "role": str(member.role)}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = await user_functions.create_refresh_token(
        data={"id": member.id, "email": member.email, "role": str(member.role)},
        expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@auth_module.post("/refresh", response_model=Token)
async def refresh_access_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    token = await user_functions.refresh_access_token(db, request.refresh_token)
    return token


# get curren user
@auth_module.get('/users/me/', response_model=User)
async def read_current_user(current_user: Annotated[User, Depends(user_functions.get_current_user)]):
    return current_user


@auth_module.get("/login/google")
async def google_login(request: Request):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_module.get("/auth/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    # Retrieve user info from Google
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)

    if not user_info:
        raise HTTPException(status_code=400, detail="Could not retrieve user info")

    # Check if user exists, else create a new user
    user = db.query(User).filter(User.email == user_info['email']).first()
    if not user:
        # Create new user in the database
        user = User(
            email=user_info['email'],
            first_name=user_info['given_name'],
            last_name=user_info['family_name'],
            role="client"  # or any default role
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Redirect to homepage or profile
    response = RedirectResponse(url='/')  # Redirect to main page
    # You can also set a session cookie for authenticated state here
    return response
