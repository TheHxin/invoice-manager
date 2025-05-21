from sqlmodel import SQLModel, Field, Relationship, ForeignKey
from decimal import Decimal
from datetime import date

class AccountParty(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : int | None = Field(default=None, unique=True, index=True)

class Invoice(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)

    amount : Decimal | None = Field(default=None)
    issued : date | None = Field(default=None)
    due : date | None = Field(default=None)

    origin_id : int | None = Field(default=None, foreign_key="accountparty.id")
    destination_id : int | None = Field(default=None, foreign_key="accountparty.id")