from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas
from app.schemas import License
from app.api.dependencies import get_db
from app.services.export_import import export_data

router = APIRouter(prefix="/licenses", tags=["licenses"])

@router.post("/", response_model=License)
def create_license(
    license: schemas.LicenseCreate,
    db: Session = Depends(get_db)
):
    """Create a new license"""
    db_license = License(**license.model_dump())
    db.add(db_license)
    db.commit()
    db.refresh(db_license)
    return db_license

@router.get("/export/")
def export_licenses(
    format: str = Query("csv", regex="^(csv|xlsx)$"),
    db: Session = Depends(get_db)
):
    """Export licenses data in specified format (csv/xlsx)"""
    licenses = db.query(License).all()
    data = [dict(l) for l in licenses]
    return export_data(data, "licenses", format)