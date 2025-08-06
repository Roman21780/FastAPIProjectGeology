from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CompanyBase(BaseModel):
    name: str = Field(
        ...,
        max_length=100,
        examples=["ООО Газпром"],
        description="Название компании (уникальное)",
        json_schema_extra={"unique": True}  # Примечание: уникальность должна проверяться на уровне БД
    )


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=100,
        examples=["ООО Газпром Нефть"],
        description="Новое название компании"
    )


class Company(CompanyBase):
    id: int = Field(
        ...,
        examples=[1],
        description="Уникальный идентификатор компании"
    )

    model_config = ConfigDict(from_attributes=True)


class WellStatusBase(BaseModel):
    name: str = Field(
        ...,
        max_length=50,
        examples=["В работе"],
        description="Название статуса скважины (уникальное)"
    )
    description: Optional[str] = Field(
        None,
        max_length=255,
        examples=["Скважина в эксплуатации"],
        description="Дополнительное описание статуса"
    )


class WellStatusCreate(WellStatusBase):
    pass


class WellStatusUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=50,
        examples=["Консервация"],
        description="Новое название статуса скважины"
    )
    description: Optional[str] = Field(
        None,
        max_length=255,
        examples=["Скважина на временной консервации"],
        description="Новое описание статуса"
    )


class WellStatus(WellStatusBase):
    id: int = Field(
        ...,
        examples=[1],
        description="Уникальный идентификатор статуса"
    )

    model_config = ConfigDict(from_attributes=True)