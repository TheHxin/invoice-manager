from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from decimal import Decimal
from typing import Optional


class InvoiceBase(SQLModel):
    amount: Decimal = Field()
    issued: date = Field()
    due: date = Field()


class InvoicePost(InvoiceBase):
    origin_id: int
    destination_id: int


class InvoiceGet(InvoiceBase):
    id: Optional[int]
    origin: str
    destination: str


class Invoice(InvoiceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    origin_id: Optional[int] = Field(default=None, foreign_key="account.id")
    destination_id: Optional[int] = Field(default=None, foreign_key="account.id")

    origin: Optional["Account"] = Relationship(
        back_populates="outgoing",
        sa_relationship_kwargs={"foreign_keys": "[Invoice.origin_id]"},
    )
    destination: Optional["Account"] = Relationship(
        back_populates="incoming",
        sa_relationship_kwargs={"foreign_keys": "[Invoice.destination_id]"},
    )


class AccountBase(SQLModel):
    name: str = Field(default=None, unique=True, index=True)


class AccountPost(AccountBase): ...


class AccountGet(AccountBase):
    id: Optional[int]


class Account(AccountBase, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True
    )  # note that the primary key columbn must be nullable in pydantic for sqlmodel to fill it out

    incoming: list[Invoice] = Relationship(
        back_populates="destination",
        sa_relationship_kwargs={"foreign_keys": "[Invoice.destination_id]"},
    )
    outgoing: list[Invoice] = Relationship(
        back_populates="origin",
        sa_relationship_kwargs={"foreign_keys": "[Invoice.origin_id]"},
    )
