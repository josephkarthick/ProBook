from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from core.company_utils import get_current_company_id
from database import get_db
from models.company import Company
from schemas.company_schema import CompanyCreate, CompanyUpdate
from services.account_setup_service import create_default_accounts


router = APIRouter(prefix="/api/companies", tags=["Companies"])


# 🔹 CREATE COMPANY
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):

    company = Company(**data.model_dump())

    db.add(company)
    db.commit()
    db.refresh(company)

    # 🔥 Automatically create default chart of accounts
    create_default_accounts(db, company.id)

    return company


# 🔹 GET ACTIVE COMPANY (FROM SESSION)
@router.get("/active")
def get_active_company(request: Request):

    company_id = request.session.get("company_id")
    company_name = request.session.get("company_name")

    if not company_id:
        return {"message": "No active company selected"}

    return {
        "company_id": company_id,
        "company_name": company_name
    }


# 🔹 LIST COMPANIES
@router.get("/")
def list_companies(db: Session = Depends(get_db)):

    companies = (
        db.query(Company)
        .filter(Company.is_active == True)
        .order_by(Company.id.desc())
        .all()
    )

    return companies


# 🔹 GET SINGLE COMPANY
@router.get("/{company_id}")
def get_company(company_id: int, db: Session = Depends(get_db)):

    company = (
        db.query(Company)
        .filter(
            Company.id == company_id,
            Company.is_active == True
        )
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


# 🔹 UPDATE COMPANY
@router.put("/{company_id}")
def update_company(company_id: int, data: CompanyUpdate, db: Session = Depends(get_db)):

    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(company, key, value)

    db.commit()
    db.refresh(company)

    return company


# 🔹 DELETE COMPANY (SOFT DELETE)
@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):

    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    company.is_active = False
    db.commit()

    return {"message": "Company deactivated successfully"}


# 🔹 SWITCH COMPANY
@router.post("/switch/{company_id}")
def switch_company(company_id: int, request: Request, db: Session = Depends(get_db)):

    company = (
        db.query(Company)
        .filter(
            Company.id == company_id,
            Company.is_active == True
        )
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # store company in session
    request.session["company_id"] = company.id
    request.session["company_name"] = company.name

    return {
        "message": f"Switched to {company.name}",
        "company_id": company.id
    }