from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class FieldBase(BaseModel):
    name: str = Field(..., max_length=100)
    license_id: int
    coordinates: Optional[str] = Field(
        None,
        pattern=r'^-?\d+\.\d+,-?\d+\.\d+$',
        examples=["55.7558,37.6176"]  # пример для документации
    )


class FieldCreate(FieldBase):
    pass


class FieldUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=100,
        examples=["Новое месторождение"]  # пример для документации
    )
    coordinates: Optional[str] = Field(
        None,
        pattern=r'^-?\d+\.\d+,-?\d+\.\d+$',
        examples=["55.7558,37.6176"]  # пример для документации
    )


class Field(FieldBase):
    id: int

    class Config:
        from_attributes = True  # или alias 'orm_mode = True' в более старых версиях