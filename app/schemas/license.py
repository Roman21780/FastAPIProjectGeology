from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class LicenseBase(BaseModel):
    number: str = Field(..., regex=r'^[A-Z]{2}-\d{4}-\d{4}$')
    issue_date: date
    expiration_date: date
    owner_id: int


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(BaseModel):
    number: Optional[str] = Field(None, regex=r'^[A-Z]{2}-\d{4}-\d{4}$')
    issue_date: Optional[date]
    expiration_date: Optional[date]
    owner_id: Optional[int]


class License(LicenseBase):
    id: int

    class Config:
        from_attributes = True