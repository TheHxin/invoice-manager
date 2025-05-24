from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
from datetime import date

class Invoice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    amount: Decimal | None = Field(default=None)
    issued: date | None = Field(default=None)
    due: date | None = Field(default=None)

    origin_id: int | None = Field(default=None, foreign_key="accountparty.id")
    destination_id: int | None = Field(default=None, foreign_key="accountparty.id")

    origin: "AccountParty" = Relationship(
        back_populates="outgoing",
        sa_relationship_kwargs={"foreign_keys": "[Invoice.origin_id]"}
    )
    destination: "AccountParty" = Relationship(
        back_populates="incoming",
        sa_relationship_kwargs={"foreign_keys": "[Invoice.destination_id]"}
    )

class AccountParty(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, unique=True, index=True)

    incoming: list["Invoice"] = Relationship(
        back_populates="destination",
        sa_relationship_kwargs={"foreign_keys": "[Invoice.destination_id]"}
    )
    outgoing: list["Invoice"] = Relationship(
        back_populates="origin",
        sa_relationship_kwargs={"foreign_keys": "[Invoice.origin_id]"}
    )
