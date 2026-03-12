from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from services.sales_return_service import create_sales_return
from schemas.sales_return_schema import SalesReturnCreate

router = APIRouter(prefix="/api", tags=["Sales Return API"])


# ===============================
# CREATE SALES RETURN
# ===============================
@router.post("/sales-returns")
def create_return(
    data: SalesReturnCreate,
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = request.session.get("company_id")

    if not company_id:
        return {"error": "No active company selected"}

    result = create_sales_return(db, data, company_id)

    return {
        "status": "success",
        "return_id": result.id,
        "return_no": result.return_no
    }