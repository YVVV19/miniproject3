from typing import Optional
from sqlmodel import Relationship, SQLModel, Field
from pydantic import field_validator, EmailStr
from . import Ads
import re


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    email: EmailStr
    password: str
    ads: Ads = Relationship(back_populates="user")

    @field_validator("name")
    @classmethod
    def name(cls, v):
        if not str(v).isalpha:
            raise ValueError("Name must include only alphabet symbols!!!")
        return v

    
    @field_validator("password")
    @classmethod
    def password(cls,v):
        if not re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"):
            raise ValueError("Your password cant go through validation")
        return v