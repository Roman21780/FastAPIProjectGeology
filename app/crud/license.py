from sqlalchemy.orm import Session
from app.models import License
from app.schemas import LicenseCreate, LicenseUpdate

def get_license(db: Session, license_id: int):
    return db.query(License).filter(License.id == license_id).first()

def get_licenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(License).offset(skip).limit(limit).all()

def create_license(db: Session, license: LicenseCreate):
    db_license = License(**license.model_dump())
    db.add(db_license)
    db.commit()
    db.refresh(db_license)
    return db_license

def update_license(db: Session, license_id: int, license: LicenseUpdate):
    db_license = get_license(db, license_id)
    if not db_license:
        return None
    update_data = license.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_license, field, value)
    db.commit()
    db.refresh(db_license)
    return db_license

def delete_license(db: Session, license_id: int):
    db_license = get_license(db, license_id)
    if not db_license:
        return None
    db.delete(db_license)
    db.commit()
    return db_license