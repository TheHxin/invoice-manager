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
    try:
        session.commit()
        session.refresh(account_party)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="AccountParty with similar name exists")
    return account_party

@router.get("/account_party/{name}")
def get_account_party(current_user: Annotated[str, Depends(getCurrentUser)], session : SessionDep, name : str):
    account_party = session.exec(select(AccountParty).where(AccountParty.name == name)).first()

    if account_party is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AccountParty not found")
    
    return account_party

@router.delete("/account_party/{id}")
def delete_account_party(current_user: Annotated[str, Depends(getCurrentUser)], session : SessionDep, id : int):
    account_party = session.get(AccountParty, id)
    if account_party is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AccountParty not found")
    
    session.delete(account_party)
    session.commit()

    return {"ok" : True}
