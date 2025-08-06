from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional


class LicenseBase(BaseModel):
    number: str = Field(
        ...,
        pattern=r'^[A-Z]{2}-\d{4}-\d{4}$',
        examples=["AB-2023-1234"],
        description="Номер лицензии в формате XX-YYYY-XXXX"
    )
    issue_date: date = Field(
        ...,
        examples=["2023-01-01"],
        description="Дата выдачи лицензии"
    )
    expiration_date: date = Field(
        ...,
        examples=["2025-01-01"],
        description="Дата окончания действия лицензии"
    )
    owner_id: int = Field(
        ...,
        examples=[1],
        description="ID компании-владельца лицензии"
    )


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(BaseModel):
    number: Optional[str] = Field(
        None,
        pattern=r'^[A-Z]{2}-\d{4}-\d{4}$',
        examples=["AB-2023-1234"],
        description="Номер лицензии в формате XX-YYYY-XXXX"
    )
    issue_date: Optional[date] = Field(
        None,
        examples=["2023-01-01"],
        description="Дата выдачи лицензии"
    )
    expiration_date: Optional[date] = Field(
        None,
        examples=["2025-01-01"],
        description="Дата окончания действия лицензии"
    )
    owner_id: Optional[int] = Field(
        None,
        examples=[1],
        description="ID компании-владельца лицензии"
    )


class License(LicenseBase):
    id: int = Field(
        ...,
        examples=[1],
        description="Уникальный идентификатор лицензии"
    )

    model_config = ConfigDict(from_attributes=True)