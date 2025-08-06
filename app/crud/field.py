from sqlalchemy.orm import Session
from app.models import Field
from app.schemas import FieldCreate, FieldUpdate

def get_field(db: Session, field_id: int):
    return db.query(Field).filter(Field.id == field_id).first()

def get_fields(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Field).offset(skip).limit(limit).all()

def create_field(db: Session, field: FieldCreate):
    db_field = Field(**field.model_dump())
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field

def update_field(db: Session, field_id: int, field: FieldUpdate):
    db_field = get_field(db, field_id)
    if not db_field:
        return None
    update_data = field.model_dump(exclude_unset=True)
    for field_name, value in update_data.items():
        setattr(db_field, field_name, value)
    db.commit()
    db.refresh(db_field)
    return db_field

def delete_field(db: Session, field_id: int):
    db_field = get_field(db, field_id)
    if not db_field:
        return None
    db.delete(db_field)
    db.commit()
    return db_field