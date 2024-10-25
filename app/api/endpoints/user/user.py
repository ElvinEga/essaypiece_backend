# fastapi 
from fastapi import APIRouter, Depends, HTTPException

# sqlalchemy
from sqlalchemy.orm import Session

# import
from app.core.dependencies import get_db, oauth2_scheme
from app.schemas.user import User, UserCreate, UserUpdate
from app.api.endpoints.user import functions as user_functions
from app.schemas.user import UserCreate, WriterProfileCreate, ClientProfileCreate
from app.api.endpoints.user.functions import create_writer_profile, create_client_profile, delete_client_profile, \
    update_client_profile, delete_writer_profile, update_writer_profile

user_module = APIRouter()


# @user_module.get('/')
# async def read_auth_page():
#     return {"msg": "Auth page Initialization done"}

# create new user 
@user_module.post('/', response_model=User)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_functions.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = user_functions.create_new_user(db, user)
    return new_user


# get all user
@user_module.get('/',
                 response_model=list[User],
                 # dependencies=[Depends(RoleChecker(['admin']))]
                 )
async def read_all_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_functions.read_all_user(db, skip, limit)


# get user by id
@user_module.get('/{user_id}',
                 response_model=User,
                 # dependencies=[Depends(RoleChecker(['admin']))]
                 )
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return user_functions.get_user_by_id(db, user_id)


# update user
@user_module.patch('/{user_id}',
                   response_model=User,
                   #   dependencies=[Depends(RoleChecker(['admin']))]
                   )
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    print(f"Received data: {user.model_dump()}")
    return user_functions.update_user(db, user_id, user)


# delete user
@user_module.delete('/{user_id}',
                    #    response_model=User,
                    #    dependencies=[Depends(RoleChecker(['admin']))]
                    )
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_functions.delete_user(db, user_id)


# @user_module.post("/users/")
# def register_user(user: UserCreate, db: Session = Depends(get_db)):
#     return create_user(user, db)


@user_module.post("/writers/profile/")
def register_writer_profile(profile: WriterProfileCreate, db: Session = Depends(get_db)):
    return create_writer_profile(profile, db)


@user_module.post("/clients/profile/")
def register_client_profile(profile: ClientProfileCreate, db: Session = Depends(get_db)):
    return create_client_profile(profile, db)


# Update writer profile
@user_module.put("/writers/profile/{writer_id}")
def update_writer_profile_endpoint(writer_id: int, profile: WriterProfileCreate, db: Session = Depends(get_db)):
    return update_writer_profile(writer_id, profile, db)


# Delete writer profile
@user_module.delete("/writers/profile/{writer_id}")
def delete_writer_profile_endpoint(writer_id: int, db: Session = Depends(get_db)):
    return delete_writer_profile(writer_id, db)


# Update client profile
@user_module.put("/clients/profile/{client_id}")
def update_client_profile_endpoint(client_id: int, profile: ClientProfileCreate, db: Session = Depends(get_db)):
    return update_client_profile(client_id, profile, db)


# Delete client profile
@user_module.delete("/clients/profile/{client_id}")
def delete_client_profile_endpoint(client_id: int, db: Session = Depends(get_db)):
    return delete_client_profile(client_id, db)
