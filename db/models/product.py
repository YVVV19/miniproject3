from typing import Optional
from sqlmodel import SQLModel, Field 
from pydantic import field_validator



class Product(SQLModel):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(..., gt=20, lt=100)
    price: float
    status: bool

    @field_validator('price')
    @classmethod
    def price(cls, v):
        if v <= 0:
            raise ValueError('Price must be over zero!!!')
        return v