from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi import Depends
from models.user import *


sql_url = "sqlite:///./data.db"
args = {"check_same_thread" : False}
engine = create_engine(sql_url, connect_args=args)

def get_session():
    with Session(engine) as session:
        yield session #to not close the session when the function has nothing to run
SessionDep = Annotated[Session, Depends(get_session)] #injects the dependency of running a specific function with meta data -> wtf? damn man