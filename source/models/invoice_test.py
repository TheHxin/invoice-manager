from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from decimal import Decimal

class AccountParty(SQLModel, table = True):
    id : int | None = Field(default=None, primary_key=True)
    name : str | None = Field(default=None)

    incoming : list["Invoice"] = Relationship(back_populates="origin")

class Invoice(SQLModel , table = True):
    id : int | None = Field(default=None, primary_key=True)
    issued : date | None = Field(default=None)
    due : date | None = Field(default=None)
    amount : Decimal | None = Field(default=None)

    origin_id : int | None = Field(default=None, foreign_key="accountparty.id")
    origin : AccountParty | None = Relationship(back_populates="incoming")
