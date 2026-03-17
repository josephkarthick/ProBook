from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from core.company_utils import get_current_company_id
from services.stock_report_service import get_low_stock_items
# services
from services.stock_report_service import get_stock_summary
from services.stock_service import stock_adjustment

router = APIRouter(prefix="/api/stock", tags=["Stock"])


# ===============================
# STOCK SUMMARY
# ===============================
@router.get("/summary")
def stock_summary(
    request: Request,
    db: Session = Depends(get_db)
):
    company_id = get_current_company_id(request)

    data = get_stock_summary(db, company_id)

    return {
        "success": True,
        "data": data
    }


# ===============================
# STOCK ADJUSTMENT
# ===============================


@router.post("/adjustment")
def adjust_stock(
    request: Request,
    payload: dict,
    db: Session = Depends(get_db)
):
    company_id = get_current_company_id(request)

    return stock_adjustment(
        db=db,
        company_id=company_id,
        item_id=payload.get("item_id"),
        qty=payload.get("qty"),
        adjustment_type=payload.get("type"),
        reason=payload.get("reason")
    )
    
    



@router.get("/low-stock")
def low_stock(request: Request, db: Session = Depends(get_db)):

    company_id = get_current_company_id(request)

    data = get_low_stock_items(db, company_id)

    return {
        "success": True,
        "data": data
    }    