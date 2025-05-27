from user_manager import router as actions_router
from invoice_manager import router as invoice_router
from auth import router as auth_router
from sqlmodel import SQLModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import *


def initDB():
    SQLModel.metadata.create_all(engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name = "static")

@app.get("/")
async def index():
    return FileResponse("static/invoice_1.html")

@app.on_event("startup") #TODO: use lifespan event handler
def on_startup():
    initDB()

app.include_router(auth_router)
app.include_router(actions_router)
app.include_router(invoice_router)