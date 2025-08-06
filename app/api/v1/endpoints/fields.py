from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Field
from app.schemas import FieldCreate, FieldUpdate
from app.api.dependencies import get_db



router = APIRouter(prefix="/fields", tags=["fields"])


@router.post("/", response_model=FieldUpdate, tags=["fields"])
def create_field(field: FieldCreate, db: Session = Depends(get_db)):
    """
    Создать новое месторождение
    """
    db_field = Field(**field.model_dump())
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field


@router.get("/", response_model=list[FieldUpdate], tags=["fields"])
def read_fields(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """
    Получить список месторождений с пагинацией
    """
    return db.query(Field).offset(skip).limit(limit).all()


@router.get("/{field_id}", response_model=FieldUpdate, tags=["fields"])
def read_field(field_id: int, db: Session = Depends(get_db)):
    """
    Получить месторождение по ID
    """
    db_field = db.query(Field).filter(Field.id == field_id).first()
    if not db_field:
        raise HTTPException(status_code=404, detail="Field not found")
    return db_field


@router.put("/{field_id}", response_model=FieldUpdate, tags=["fields"])
def update_field(
        field_id: int,
        field: FieldUpdate,
        db: Session = Depends(get_db)
):
    """
    Обновить месторождение
    """
    db_field = db.query(Field).filter(Field.id == field_id).first()
    if not db_field:
        raise HTTPException(status_code=404, detail="Field not found")

    update_data = field.model_dump(exclude_unset=True)
    for field_name, value in update_data.items():
        setattr(db_field, field_name, value)

    db.commit()
    db.refresh(db_field)
    return db_field


@router.delete("/{field_id}", tags=["fields"])
def delete_field(field_id: int, db: Session = Depends(get_db)):
    """
    Удалить месторождение
    """
    db_field = db.query(Field).filter(Field.id == field_id).first()
    if not db_field:
        raise HTTPException(status_code=404, detail="Field not found")

    db.delete(db_field)
    db.commit()
    return {"message": "Field deleted successfully"}