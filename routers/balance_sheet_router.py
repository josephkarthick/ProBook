from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from services.balance_sheet_service import get_balance_sheet

router = APIRouter(prefix="/balance-sheet", tags=["Balance Sheet"])


@router.get("/")
def balance_sheet(request: Request, db: Session = Depends(get_db)):

    company_id = request.session.get("company_id")

    return get_balance_sheet(db, company_id)