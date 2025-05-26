from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from auth import getCurrentUser
from sqlmodel import select
from models.invoice import *
from database import *


router = APIRouter()


@router.post("/account_party")
def post_account_party(current_user: Annotated[str, Depends(getCurrentUser)],account_party : AccountParty, session : SessionDep) -> AccountParty:
    db_account_party = AccountParty()
    db_account_party.name = account_party.name

    session.add(db_account_party)
    try:
        session.commit()
        session.refresh(db_account_party)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="AccountParty with same name exists")
    return db_account_party

@router.get("/account_parties")
def get_account_parties(current_user: Annotated[str, Depends(getCurrentUser)], session : SessionDep) -> list[AccountParty]:
    account_party_list = session.exec(select(AccountParty)).all()
    account_party_list = list(account_party_list)
    return account_party_list

@router.get("/account_party/{name}")
def get_account_party_name(current_user: Annotated[str, Depends(getCurrentUser)], session : SessionDep, name : str) -> AccountParty:
    account_party = session.exec(select(AccountParty).where(AccountParty.name == name)).first()

    if account_party is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AccountParty not found")
    
    return account_party

@router.delete("/account_party/{id}")
def delete_account_party(current_user: Annotated[str, Depends(getCurrentUser)], session : SessionDep, id : int):
    account_party = session.get(AccountParty, id)
    if account_party is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AccountParty not found")
    try:
        session.delete(account_party)
        session.commit()
        return {"ok" : True}

    except:
        return {"ok" : False}
    

#---------------------------------------------------------------------------------

@router.post("/invoice")
def post_invoice(current_user : Annotated[str, Depends(getCurrentUser)], session : SessionDep, invoice : Invoice) -> Invoice:
    db_invoice = Invoice()
    db_invoice.amount = invoice.amount
    db_invoice.due = invoice.due
    db_invoice.issued = invoice.issued
    db_invoice.origin = invoice.origin
    db_invoice.destination = invoice.destination

    session.add(db_invoice)
    session.commit()
    session.refresh(db_invoice)
    
    return db_invoice

@router.get("/invoices")
def get_invoices(current_user : Annotated[str, Depends(getCurrentUser)], session : SessionDep) -> list[Invoice]:
    invoice_list = session.exec(select(Invoice)).all()
    invoice_list = list(invoice_list)
    return invoice_list

@router.delete("/invoice/{id}")
def delete_invoice(current_user : Annotated[str, Depends(getCurrentUser)], session : SessionDep, id : int):
    invoice_found = session.get(Invoice,id)
    if invoice_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    try:
        session.delete(invoice_found)
        session.commit()
        return {"ok" : True}

    except:
        return {"ok" : False}