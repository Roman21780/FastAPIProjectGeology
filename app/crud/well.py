from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Well
from app.schemas import WellCreate, WellUpdate

def get_well(db: Session, well_id: int):
    return db.query(Well).filter(Well.id == well_id).first()

def get_wells(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Well).offset(skip).limit(limit).all()

def create_well(db: Session, well: WellCreate):
    db_well = Well(**well.model_dump())
    db.add(db_well)
    db.commit()
    db.refresh(db_well)
    return db_well


def update_well(db: Session, well_id: int, well: WellUpdate):
    db_well = get_well(db, well_id)
    if not db_well:
        raise HTTPException(status_code=404, detail="Well not found")  # Добавлена проверка

    update_data = well.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_well, field, value)
    db.commit()
    db.refresh(db_well)
    return db_well

def delete_well(db: Session, well_id: int):
    db_well = get_well(db, well_id)
    if not db_well:
        return None
    db.delete(db_well)
    db.commit()
    return db_well