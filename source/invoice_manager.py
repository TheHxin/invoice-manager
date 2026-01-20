from fastapi import APIRouter, HTTPException, status, Response
from sqlalchemy.exc import IntegrityError
from auth import getCurrentUser
from sqlmodel import select
from models.invoice import *
from database import *


router = APIRouter()


@router.post("/account", status_code=status.HTTP_201_CREATED)
def post_account(current_user: Annotated[str, Depends(getCurrentUser)],account : AccountPost, session : SessionDep) -> Account:
    account_db = Account(**account.model_dump())
    session.add(account_db)
    try:
        session.commit()
        session.refresh(account_db)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Account with same name exists")
    return account_db

@router.get("/accounts", status_code=status.HTTP_200_OK)
def get_accounts(current_user: Annotated[str, Depends(getCurrentUser)], session : SessionDep) -> list[Account]:
    accounts = session.exec(select(Account)).all()
    accounts = list(accounts)
    return accounts

@router.get("/account/{name}", status_code=status.HTTP_200_OK)
def get_account(current_user: Annotated[str, Depends(getCurrentUser)], session : SessionDep, name : str) -> Account:
    account = session.exec(select(Account).where(Account.name == name)).first()

    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found with the given name")
    
    return account

@router.delete("/account/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.post("/invoice", status_code=status.HTTP_201_CREATED)
def post_invoice(current_user : Annotated[str, Depends(getCurrentUser)], session : SessionDep, invoice : InvoicePost) -> Invoice:

    #if either origin or destination accounts do not exist raise an http error
#    if (not accountExists(invoice.origin_id, session)) and (not accountExists(invoice.destination_id, session)):
#        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="origin_id or destination_id object does not exist in the DB")

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

#checks if an account exsits
def accountExists(account_id : int, session : SessionDep) -> bool:
    return (session.exec(select(Account.id).where(Account.id == account_id)).first() is None) or (session.exec(select(Account.id).where(Account.id == account_id)).first() is None)

@router.get("/invoices", status_code=status.HTTP_200_OK)
def get_invoices(current_user : Annotated[str, Depends(getCurrentUser)], session : SessionDep) -> list[InvoiceGet]:
    invoices_db = list(session.exec(select(Invoice)).all())
    
    invoices_response = []
    for invoice_db in invoices_db:
        invoices_response.append(
            InvoiceGet(
                id=invoice_db.id,
                origin_name=invoice_db.origin.name,
                destination_name=invoice_db.destination.name,
                amount=invoice_db.amount,
                due=invoice_db.due,
                issued=invoice_db.issued
            )
        )
    
    return invoices_response

@router.delete("/invoice/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
    

