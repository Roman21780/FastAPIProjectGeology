from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.api.dependencies import get_db
from app.schemas import CompanyUpdate

router = APIRouter(prefix="/references", tags=["references"])

@router.post("/companies/", response_model=schemas.Company, tags=["references"])
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    return crud.create_company(db=db, company=company)

@router.get("/companies/", response_model=list[schemas.Company], tags=["references"])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_companies(db=db, skip=skip, limit=limit)

@router.patch("/companies/{company_id}", response_model=schemas.Company, tags=["references"])
def update_company(
    company_id: int,
    company: CompanyUpdate,
    db: Session = Depends(get_db)
):
    db_company = crud.update_company(db, company_id=company_id, company=company)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.post("/statuses/", response_model=schemas.WellStatus, tags=["references"])
def create_status(status: schemas.WellStatusCreate, db: Session = Depends(get_db)):
    return crud.create_well_status(db=db, status=status)

@router.get("/statuses/", response_model=list[schemas.WellStatus], tags=["references"])
def read_statuses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_well_statuses(db=db, skip=skip, limit=limit)