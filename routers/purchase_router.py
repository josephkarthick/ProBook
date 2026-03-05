from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from core.company_utils import get_current_company_id

from schemas.purchase_schema import PurchaseBillCreate
from services.purchase_service import create_purchase_bill


router = APIRouter(prefix="/purchases", tags=["Purchases"])


@router.post("/")
def create_purchase_api(
    data: PurchaseBillCreate,
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    return create_purchase_bill(db, data, company_id)