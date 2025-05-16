from sqlmodel import Field, SQLModel,  create_engine, select, Session
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from models.user import *

from sqlalchemy.exc import IntegrityError

from jwt_test import hashPassword

app = FastAPI()

sql_url = "sqlite:///./data.db"
args = {"check_same_thread" : False}
engine = create_engine(sql_url, connect_args=args)

def get_session():
    with Session(engine) as session:
        yield session #to not close the session when the function has nothing to run

SessionDep = Annotated[Session, Depends(get_session)] #injects the dependency of running a specific function with meta data -> wtf? damn man

def initDB():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup") #TODO: use lifespan event handler
def on_startup():
    initDB()

#TODO: add JWT user authntication
# @app.post("/auth")
# def auth_user():
#     ...

@app.post("/user")
def post_user(user: UserPost, session: SessionDep) -> UserBase:

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

@app.get("/users")
def get_users(session: SessionDep) -> list[UserBase]:
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

@app.get("/user/{username}")
def get_user_username(username : str, session : SessionDep) -> UserBase:
    user_db = session.exec(select(User).where(User.username == username)).first()  #note: we defined username column as unique but the select will return a list of one elemtn with .first we get the first and only obj in the list
    user_return = UserBase()
    
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_return.id = user_db.id
    user_return.username = user_db.username
    user_return.email = user_db.email
    user_return.full_name = user_db.full_name

    return user_return

@app.delete("/user/{id}")
def delete_user(id: int, session: SessionDep):
    try:
        user = session.get(User, id) #note: session.get is used to get an obj by primary key only and will return only one row
        session.delete(user)
        session.commit()

        return {"ok" : True}
    except:
        return {"ok" : False}