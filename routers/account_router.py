from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.accounts import Account
from core.company_utils import get_current_company_id
from schemas.account_schema import AccountCreate, AccountResponse

router = APIRouter(prefix="/accounts", tags=["Accounts"])



@router.get("/")
def list_accounts(request: Request, db: Session = Depends(get_db)):
    company_id = get_current_company_id(request)

    return db.query(Account)\
             .filter(Account.company_id == company_id)\
             .order_by(Account.id)\
             .all()
             
@router.post("/", response_model=AccountResponse)
def create_account(
    request: Request,
    account: AccountCreate,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    parent_id = account.parent_id

    # ✅ Validate parent account
    if parent_id:

        parent = db.query(Account).filter(
            Account.id == parent_id,
            Account.company_id == company_id
        ).first()

        if not parent:
            raise HTTPException(
                status_code=400,
                detail="Invalid parent account"
            )

    new_account = Account(
        company_id=company_id,
        name=account.name,
        account_code=account.account_code,
        account_type=account.account_type,
        parent_id=parent_id,
        is_group=account.is_group,
        opening_balance=account.opening_balance,
        opening_type=account.opening_type
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

@router.put("/{account_id}")
def update_account(account_id: int,
                   data: dict,
                   request: Request,
                   db: Session = Depends(get_db)):

    company_id = get_current_company_id(request)

    account = db.query(Account).filter(
        Account.id == account_id,
        Account.company_id == company_id
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if account.is_system:
        raise HTTPException(status_code=400, detail="System account cannot be edited")

    account.name = data.get("name", account.name)
    db.commit()
    db.refresh(account)

    return account

@router.delete("/{account_id}")
def delete_account(account_id: int,
                   request: Request,
                   db: Session = Depends(get_db)):

    company_id = get_current_company_id(request)

    account = db.query(Account).filter(
        Account.id == account_id,
        Account.company_id == company_id
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if account.is_system:
        raise HTTPException(status_code=400, detail="System account cannot be deleted")

    db.delete(account)
    db.commit()

    return {"message": "Deleted successfully"}    