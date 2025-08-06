from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class WellBase(BaseModel):
    name: str = Field(..., max_length=100)
    depth: float = Field(..., gt=0)
    status_id: int
    drilling_date: date
    license_id: int
    field_id: int


class WellCreate(WellBase):
    pass


class WellUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    depth: Optional[float] = Field(None, gt=0)
    status_id: Optional[int]


class Well(WellBase):
    id: int

    class Config:
        from_attributes = True