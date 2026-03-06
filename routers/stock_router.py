from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from core.company_utils import get_current_company_id
from services.stock_report_service import get_stock_summary

router = APIRouter(prefix="/stock", tags=["Stock"])


@router.get("/summary")
def stock_summary(
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    return get_stock_summary(db, company_id)