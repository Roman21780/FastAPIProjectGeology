from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Well)
def create_well(well: schemas.WellCreate, db: Session = Depends(get_db)):
    return crud.well.create(db, obj_in=well)

@router.get("/", response_model=list[schemas.Well])
def read_wells(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.well.get_multi(db, skip=skip, limit=limit)

@router.get("/{well_id}", response_model=schemas.Well)
def read_well(well_id: int, db: Session = Depends(get_db)):
    db_well = crud.well.get(db, id=well_id)
    if not db_well:
        raise HTTPException(status_code=404, detail="Well not found")
    return db_well

@router.put("/{well_id}", response_model=schemas.Well)
def update_well(well_id: int, well: schemas.WellUpdate, db: Session = Depends(get_db)):
    return crud.well.update(db, id=well_id, obj_in=well)

@router.delete("/{well_id}")
def delete_well(well_id: int, db: Session = Depends(get_db)):
    return crud.well.remove(db, id=well_id)