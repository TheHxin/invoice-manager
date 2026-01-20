from user_manager import router as actions_router
from invoice_manager import router as invoice_router
from auth import router as auth_router
from sqlmodel import SQLModel
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from database import *
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


def initDB():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):  # runs the code before "yeild" before app startup and runs the code after yeild at shutdown
    initDB()  # startup code here

    yield

    # shutdown code here


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["http://localhost:5173","http://localhost:4173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index(request: Request):
    return RedirectResponse(str(request.base_url) + "docs")
    #return FileResponse("static/invoice_1.html")


app.include_router(auth_router)
app.include_router(actions_router)
app.include_router(invoice_router)
