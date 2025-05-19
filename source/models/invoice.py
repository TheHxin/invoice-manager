from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
from datetime import date
from typing import Optional, List

class AccountParty(SQLModel, table=True):
    id : int = Field(default=None, primary_key=True)
    name : str = Field(default=None, index=True)
    incoming : List["Invoice"] = Relationship(back_populates="destination") #Why Invoice in "" becuase Invoice is not defined yet and is a forward refrencing
    outgoing : List["Invoice"] = Relationship(back_populates="origin")

class Invoice(SQLModel, table=True):
    id : int = Field(default=None, primary_key=True)
    origin : Optional[AccountParty] = Relationship(back_populates="outgoing")
    destination : Optional[AccountParty] = Relationship(back_populates="incoming")
    Amount : Decimal = Field(default=None)
    issued : date = Field(default=None)
    due : date = Field(default=None)
    
