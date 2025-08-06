from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import schemas
from app.api.dependencies import get_db
from app.models import Well

router = APIRouter(prefix="/wells", tags=["wells"])

@router.post("/", response_model=schemas.Well)
def create_well(well: schemas.WellCreate, db: Session = Depends(get_db)):
    """Create a new well"""
    db_well = Well(**well.model_dump())
    db.add(db_well)
    db.commit()
    db.refresh(db_well)
    return db_well


@router.get("/", response_model=List[schemas.Well])
def read_wells(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """Get list of wells with pagination"""
    return db.query(Well).offset(skip).limit(limit).all()


@router.get("/{well_id}", response_model=schemas.Well)
def read_well(well_id: int, db: Session = Depends(get_db)):
    """Get well by ID"""
    db_well = db.query(Well).filter(Well.id == well_id).first()
    if not db_well:
        raise HTTPException(status_code=404, detail="Well not found")
    return db_well


@router.put("/{well_id}", response_model=schemas.Well)
def update_well(
        well_id: int,
        well: schemas.WellUpdate,
        db: Session = Depends(get_db)
):
    """Update well information"""
    db_well = db.query(Well).filter(Well.id == well_id).first()
    if not db_well:
        raise HTTPException(status_code=404, detail="Well not found")

    update_data = well.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_well, field, value)

    db.commit()
    db.refresh(db_well)
    return db_well


@router.delete("/{well_id}")
def delete_well(well_id: int, db: Session = Depends(get_db)):
    """Delete a well"""
    db_well = db.query(Well).filter(Well.id == well_id).first()
    if not db_well:
        raise HTTPException(status_code=404, detail="Well not found")

    db.delete(db_well)
    db.commit()
    return {"message": "Well deleted successfully"}