from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime

class AuthorCreate(BaseModel):
    name: str
    country: Optional[str] = None

class AuthorResponse(BaseModel):
    id: int
    name: str
    country: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class BookCreate(BaseModel):
    title: str
    year: int = Field(..., ge=1000, le=datetime.now().year)
    author_id: int

    @field_validator('year')
    @classmethod
    def year_must_not_be_future(cls, v):
        if v > datetime.now().year:
            raise ValueError(f'Year cannot be greater than {datetime.now().year}')
        return v

class BookResponse(BaseModel):
    id: int
    title: str
    year: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)