from pydantic import BaseModel, Field
from typing import Optional


class CompanyBase(BaseModel):
    name: str = Field(..., max_length=100, unique=True)


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)


class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True


class WellStatusBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = Field(None, max_length=255)


class WellStatusCreate(WellStatusBase):
    pass


class WellStatusUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=255)


class WellStatus(WellStatusBase):
    id: int

    class Config:
        from_attributes = True