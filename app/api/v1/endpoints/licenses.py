from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.crud import license as crud
from app.schemas import License, LicenseCreate, LicenseUpdate
from app.api.dependencies import get_db
from app.services.export_import import export_data

router = APIRouter()

@router.post("/", response_model=License)
def create_license(license: LicenseCreate, db: Session = Depends(get_db)):
    return crud.create_license(db, license)

@router.get("/export/")
def export_licenses(
    format: str = Query("csv", regex="^(csv|xlsx)$"),
    db: Session = Depends(get_db)
):
    licenses = crud.get_licenses(db)
    data = [dict(l) for l in licenses]
    return export_data(data, "licenses", format)