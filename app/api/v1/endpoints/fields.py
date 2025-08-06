from fastapi import Depends, HTTPException, APIRouter
from app import crud, schemas
from sqlalchemy.orm import Session
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Field)
def create_field(field: schemas.FieldCreate, db: Session = Depends(get_db)):
    return crud.field.create(db, obj_in=field)

@router.get("/", response_model=list[schemas.Field])
def read_fields(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.field.get_multi(db, skip=skip, limit=limit)

@router.get("/{field_id}", response_model=schemas.Field)
def read_field(field_id: int, db: Session = Depends(get_db)):
    db_field = crud.field.get(db, id=field_id)
    if not db_field:
        raise HTTPException(status_code=404, detail="Field not found")
    return db_field

@router.put("/{field_id}", response_model=schemas.Field)
def update_field(field_id: int, field: schemas.FieldUpdate, db: Session = Depends(get_db)):
    return crud.field.update(db, id=field_id, obj_in=field)

@router.delete("/{field_id}")
def delete_field(field_id: int, db: Session = Depends(get_db)):
    return crud.field.remove(db, id=field_id)