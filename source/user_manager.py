from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from auth import hashPassword, getCurrentUser
from sqlmodel import select
from models.user import *
from database import *


router = APIRouter()


@router.post("/user")
def post_user(current_user: Annotated[str, Depends(getCurrentUser)], user: UserPost, session: SessionDep) -> UserBase:

    user_db = User()
    user_db.username = user.username
    user_db.password_hashed = hashPassword(user.password)
    user_db.full_name = user.full_name
    user_db.email = user.email

    session.add(user_db)
    try:
        session.commit()
        session.refresh(user_db)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user_return = UserBase()
    user_return.id = user_db.id
    user_return.username = user_db.username
    user_return.email = user_db.email
    user_return.full_name = user_db.full_name

    return user_return

@router.get("/users")
def get_users(current_user: Annotated[str, Depends(getCurrentUser)], session: SessionDep) -> list[UserBase]:
    users_db = session.exec(select(User)).all()
    users_return = []
    for user_db in users_db:
        user_return = UserBase()
        user_return.id = user_db.id
        user_return.username = user_db.username
        user_return.email = user_db.email
        user_return.full_name = user_db.full_name

        users_return.append(user_return)
    
    return users_return

@router.get("/user/{username}")
def get_user_username(current_user: Annotated[str, Depends(getCurrentUser)], username : str, session : SessionDep) -> UserBase:
    user_db = session.exec(select(User).where(User.username == username)).first()  #note: we defined username column as unique but the select will return a list of one elemtn with .first we get the first and only obj in the list
    user_return = UserBase()
    
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_return.id = user_db.id
    user_return.username = user_db.username
    user_return.email = user_db.email
    user_return.full_name = user_db.full_name

    return user_return

@router.delete("/user/{id}")
def delete_user(current_user: Annotated[str, Depends(getCurrentUser)], id: int, session: SessionDep):
    try:
        user = session.get(User, id) #note: session.get is used to get an obj by primary key only and will return only one row
        session.delete(user)
        session.commit()

        return {"ok" : True}
    except:
        return {"ok" : False}