from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from auth import getCurrentUser
from sqlmodel import select
from models.invoice import *
from database import *


router = APIRouter()


@router.post("/account_party")
def post_account_party(current_user: Annotated[str, Depends(getCurrentUser)],account_party : AccountParty, session : SessionDep):
    session.add(account_party)
    session.commit()
    session.refresh(account_party)
    return account_party

@router.get("/account_party/{name}")
def get_account_party(current_user: Annotated[str, Depends(getCurrentUser)], session : SessionDep, name : str):
    account_party = session.exec(select(AccountParty).where(AccountParty.name == name)).first()
    