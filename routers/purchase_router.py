from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from schemas.purchase_schema import PurchaseBillCreate
from services.purchase_service import create_purchase_bill
from core.company_utils import get_current_company_id
from schemas.item_schema import ItemCreate

router = APIRouter(prefix="/purchases", tags=["Purchases"])

    
@router.post("/")
def create_item_api(
    data: ItemCreate,
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    return create_item(db, data, company_id)    