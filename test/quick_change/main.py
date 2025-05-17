from useractions import router as actions_router
from jwt_test2 import router as auth_router
from sqlmodel import SQLModel
from fastapi import FastAPI
from database import *


def initDB():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup") #TODO: use lifespan event handler
def on_startup():
    initDB()

app.include_router(auth_router)
app.include_router(actions_router)