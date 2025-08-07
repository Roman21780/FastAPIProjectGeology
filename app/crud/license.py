from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import License
from app.schemas import LicenseCreate, LicenseUpdate
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


def get_license(db: Session, license_id: int) -> Optional[License]:
    """Get a single license by ID"""
    try:
        return db.query(License).filter(License.id == license_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error getting license {license_id}: {str(e)}")
        raise


def get_licenses(db: Session, skip: int = 0, limit: int = 100) -> List[License]:
    """Get list of licenses with pagination"""
    try:
        return db.query(License).order_by(License.id).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error getting licenses: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Database error while fetching licenses"
        )


def create_license(db: Session, license: LicenseCreate) -> License:
    """Create a new license"""
    try:
        db_license = License(**license.model_dump())
        db.add(db_license)
        db.commit()
        db.refresh(db_license)
        return db_license
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating license: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating license: {str(e)}")
        raise


def update_license(
        db: Session,
        license_id: int,
        license: LicenseUpdate
) -> Optional[License]:
    """Update an existing license"""
    try:
        db_license = get_license(db, license_id)
        if not db_license:
            return None

        update_data = license.model_dump(exclude_unset=True)

        # Validate number format if being updated
        if 'number' in update_data:
            if not update_data['number'] or len(update_data['number']) < 5:
                raise ValueError("License number must be at least 5 characters")

        for field, value in update_data.items():
            setattr(db_license, field, value)

        db.commit()
        db.refresh(db_license)
        return db_license

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating license {license_id}: {str(e)}")
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error updating license: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error updating license: {str(e)}")
        raise


def delete_license(db: Session, license_id: int) -> Optional[License]:
    """Delete a license"""
    try:
        db_license = get_license(db, license_id)
        if not db_license:
            return None

        db.delete(db_license)
        db.commit()
        return db_license

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting license {license_id}: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error deleting license: {str(e)}")
        raise