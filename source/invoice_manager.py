from fastapi import APIRouter, HTTPException, status, Response
from sqlalchemy.exc import IntegrityError
from auth import getCurrentUser
from sqlmodel import select
from models.invoice import *
from database import *


router = APIRouter()


@router.post("/account") #updated
def post_account(current_user: Annotated[str, Depends(getCurrentUser)],account : AccountPost, session : SessionDep) -> Account:
    account_db = Account(**account.dict())
    session.add(account_db)
    try:
        session.commit()
        session.refresh(account_db)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Account with same name exists")
    return account_db

@router.get("/accounts") #updated
def get_account_parties(current_user: Annotated[str, Depends(getCurrentUser)], session : SessionDep) -> list[Account]:
    accounts = session.exec(select(Account)).all()
    accounts = list(accounts)
    return accounts

@router.get("/account/{name}") #updated
def get_account_name(current_user: Annotated[str, Depends(getCurrentUser)], session : SessionDep, name : str) -> Account:
    account = session.exec(select(Account).where(Account.name == name)).first()

    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found with the given name")
    
    return account

@router.delete("/account/{id}", status_code=status.HTTP_204_NO_CONTENT) #updated
def delete_account(current_user: Annotated[str, Depends(getCurrentUser)], session : SessionDep, id : int):
    account = session.get(Account, id)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found with the given id")
    try:
        session.delete(account)
        session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(e))
    


#---------------------------------------------------------------------------------



@router.post("/invoice") #updated
def post_invoice(current_user : Annotated[str, Depends(getCurrentUser)], session : SessionDep, invoice : InvoicePost) -> Invoice:
    if session.exec(select(Account.id).where(Account.id == invoice.origin_id)).first() is None or session.exec(select(Account.id).where(Account.id == invoice.destination_id)).first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="origin_id or destination_id object does not exist in the DB")

    invoice_db = Invoice(
        amount=invoice.amount,
        issued=invoice.issued,
        due=invoice.due,
        origin_id=invoice.origin_id,
        destination_id=invoice.destination_id
    )
    session.add(invoice_db)
    session.commit()
    session.refresh(invoice_db)
    return invoice_db

@router.get("/invoices") #updated
def get_invoices(current_user : Annotated[str, Depends(getCurrentUser)], session : SessionDep) -> list[Invoice]:
    invoices_db = list(session.exec(select(Invoice)).all())
    invoices = []
    for invoice in invoices_db:
        if invoice.origin is None or invoice.destination is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="the origin or destination can not be null -> this is a db error contact developer",
            )

        invoices.append(
            InvoiceGet(
                id=invoice.id,
                amount=invoice.amount,
                due=invoice.due,
                issued=invoice.issued,
                origin=invoice.origin.name,
                destination=invoice.destination.name,
            )
        )

    return invoices

@router.delete("/invoice/{id}", status_code=status.HTTP_204_NO_CONTENT) #TODO: do 2 o 4 for deletes
def delete_invoice(current_user : Annotated[str, Depends(getCurrentUser)], session : SessionDep, id : int):
    invoice_found = session.get(Invoice,id)
    if invoice_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    try:
        session.delete(invoice_found)
        session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(e))