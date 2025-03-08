from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from . import User, Product
from pydantic import field_validator


class Ads(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    user: User = Relationship(back_populates="ads")
    product: Product = Relationship(back_populates="ads")
