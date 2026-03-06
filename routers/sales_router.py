from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from services.sales_service import create_sales_invoice
from schemas.sales_schema import SalesInvoiceCreate

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("/")
def create_sales_api(
    data: SalesInvoiceCreate,
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = request.session.get("company_id")

    return create_sales_invoice(
        db,
        data,
        company_id
    )