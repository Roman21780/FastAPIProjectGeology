from sqlalchemy.orm import Session

from app import schemas
from app.models import Company, WellStatus
from app.schemas import CompanyCreate, WellStatusCreate, WellStatusUpdate

# Операции для компаний
def get_company(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: CompanyCreate):
    db_company = Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company: schemas.CompanyUpdate):
    db_company = get_company(db, company_id)
    if not db_company:
        return None
    update_data = company.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_company, field, value)
    db.commit()
    db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    db_company = get_company(db, company_id)
    if not db_company:
        return None
    db.delete(db_company)
    db.commit()
    return db_company

# Операции для статусов скважин
def get_well_status(db: Session, status_id: int):
    return db.query(WellStatus).filter(WellStatus.id == status_id).first()

def get_well_statuses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(WellStatus).offset(skip).limit(limit).all()

def create_well_status(db: Session, status: WellStatusCreate):
    db_status = WellStatus(**status.model_dump())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

def update_well_status(db: Session, status_id: int, status: WellStatusUpdate):
    db_status = get_well_status(db, status_id)
    if not db_status:
        return None
    update_data = status.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_status, field, value)
    db.commit()
    db.refresh(db_status)
    return db_status

def delete_well_status(db: Session, status_id: int):
    db_status = get_well_status(db, status_id)
    if not db_status:
        return None
    db.delete(db_status)
    db.commit()
    return db_status