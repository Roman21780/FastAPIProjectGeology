from pydantic import BaseModel
from datetime import date
from typing import Optional

from app.models import Field


class FieldBase(BaseModel):
    name: str = Field(..., max_length=100)
    license_id: int
    coordinates: Optional[str] = Field(None, regex=r'^-?\d+\.\d+,-?\d+\.\d+$')


class FieldCreate(FieldBase):
    pass


class FieldUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    coordinates: Optional[str] = Field(None, regex=r'^-?\d+\.\d+,-?\d+\.\d+$')


class Field(FieldBase):
    id: int

    class Config:
        from_attributes = True