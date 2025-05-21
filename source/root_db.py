from models.user import *
from models.invoice import *
from database import *
from sqlmodel import SQLModel, select
from auth import hashPassword
from decimal import Decimal


def create_tables():
    SQLModel.metadata.create_all(engine)

def add_user(username, password):
    with Session(engine) as session:
        user = User()
        user.username = username
        user.password_hashed = hashPassword(password)
        user.full_name = "manually added"
        user.email = "manually added"

        session.add(user)
        session.commit()
        session.refresh(user)

def add_accountparty(name):
    with Session(engine) as session:
        accountparty = AccountParty()
        accountparty.name = name

        session.add(accountparty)
        session.commit()
        session.refresh(accountparty)

def add_invoice(amount : Decimal, issued : date, due : date, origin : AccountParty | None, destination : AccountParty | None):
    with Session(engine) as session:
        invoice = Invoice()
        invoice.amount = amount
        invoice.issued = issued
        invoice.due = due
        invoice.origin = origin
        invoice.destination = destination

        session.add(invoice)
        session.commit()
        session.refresh(invoice)


create_tables()
add_user("root","root1234")
add_accountparty("intel")
add_accountparty("amd")
add_accountparty("nvidia")
with Session(engine) as session:
    origin = session.exec(select(AccountParty).where(AccountParty.name == "intel")).first()
    destination = session.exec(select(AccountParty).where(AccountParty.name == "amd")).first()
add_invoice(amount=Decimal(123.12), 
            issued=date(2000,2,2), 
            due=date(2001,2,2), 
            origin=origin, 
            destination=destination)