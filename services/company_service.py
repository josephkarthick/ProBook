from sqlalchemy.orm import Session
from models.company import Company
from services.account_setup_service import create_default_accounts


def create_company(db: Session, company_data):

    # create company
    new_company = Company(**company_data.model_dump())

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    # 🔥 IMPORTANT — create accounts AFTER company exists
    create_default_accounts(db, new_company.id)

    return new_company