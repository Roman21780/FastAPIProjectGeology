from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from starlette.responses import FileResponse, StreamingResponse

from app import schemas
from app.api.dependencies import get_db
from app.core.logging import logger
from app.crud import license as license_crud
from app.services.export_import import export_data

router = APIRouter(prefix="/licenses", tags=["licenses"])

@router.post("/", response_model=schemas.License, status_code=status.HTTP_201_CREATED)
def create_license(
    license: schemas.LicenseCreate,
    db: Session = Depends(get_db)
):
    """Create a new license"""
    return license_crud.create_license(db=db, license=license)

@router.get("/", response_model=List[schemas.License])
def read_licenses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retrieve all licenses"""
    return license_crud.get_licenses(db, skip=skip, limit=limit)

@router.get("/{license_id}", response_model=schemas.License)
def read_license(
    license_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific license by ID"""
    db_license = license_crud.get_license(db, license_id=license_id)
    if db_license is None:
        raise HTTPException(status_code=404, detail="License not found")
    return db_license

@router.put("/{license_id}", response_model=schemas.License)
def update_license(
    license_id: int,
    license: schemas.LicenseUpdate,
    db: Session = Depends(get_db)
):
    """Update a license"""
    db_license = license_crud.update_license(db, license_id=license_id, license=license)
    if db_license is None:
        raise HTTPException(status_code=404, detail="License not found")
    return db_license

@router.delete("/{license_id}", response_model=schemas.License)
def delete_license(
    license_id: int,
    db: Session = Depends(get_db)
):
    """Delete a license"""
    db_license = license_crud.delete_license(db, license_id=license_id)
    if db_license is None:
        raise HTTPException(status_code=404, detail="License not found")
    return db_license


@router.get("/export/", response_class=StreamingResponse)
def export_licenses(
        format: str = Query("csv", regex="^(csv|xlsx)$"),
        db: Session = Depends(get_db)
):
    """Export licenses data in specified format (csv/xlsx)"""
    try:
        licenses = license_crud.get_licenses(db)
        if not licenses:
            raise HTTPException(
                status_code=404,
                detail="No licenses found to export"
            )

        # Convert SQLAlchemy models to dicts
        data = [license.__dict__ for license in licenses]

        # Remove SQLAlchemy internal attributes
        for item in data:
            item.pop('_sa_instance_state', None)

        return export_data(data, "licenses", format)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"License export failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"License export failed: {str(e)}"
        )