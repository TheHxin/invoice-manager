from models.user import *
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from models.user import *

from datetime import datetime, timedelta, timezone

from sqlmodel import Field, SQLModel,  create_engine, select, Session
from pydantic import BaseModel

sql_url = "sqlite:///./data.db"
args = {"check_same_thread" : False}
engine = create_engine(sql_url, connect_args=args)

SECRET_KEY = "11796b3a061734e7e1b67b25ad8226b5f6a2ce983175757a9b10d413d0e29c45"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session #to not close the session when the function has nothing to run
SessionDep = Annotated[Session, Depends(get_session)] #injects the dependency of running a specific function with meta data -> wtf? damn man

class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None

def hashPassword(password):
    return pwd_context.hash(password)
def verifyPassword(password, hashed_password):
    return pwd_context.verify(password,hashed_password)


def createToken(data: dict, expire_delta: timedelta = timedelta(minutes=15)): #expire_delta = is the offset from the now to the time it should expire (like in 2 days)
    data_copy = data.copy() #copy the data to manipulate it without touching data dict
    expire = datetime.now(timezone.utc) + expire_delta
    data_copy.update({"exp" : expire})
    encoded_jwt = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def getCurrentUser(token: Annotated[str, Depends(oauth2_scheme)], session : Session): #does not need to be async as uvicorn will make a coroutine for it auto

    credintials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate creds",
        headers={"WWW-Authenticate" : "Bearer"})
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credintials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credintials_exception
    
    user_db = session.exec(select(User).where(User.username == token_data.username)).first()
    if user_db is None:
        raise credintials_exception

    user_return = UserBase()
    user_return.id = user_db.id
    user_return.username = user_db.username
    user_return.email = user_db.email
    user_return.full_name = user_db.full_name

    return user_return


@app.post("/token")
async def login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    
    user = session.exec(select(User).where(User.username == form_data.username)).first() 
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verifyPassword(form_data.password, user.password_hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cred not valid -> incorrect username or password",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = createToken(
        data={"sub" : user.username},
        expire_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me")
def getMe(token: Annotated[str, Depends(oauth2_scheme)], session : SessionDep):
    return getCurrentUser(token=token, session=session)