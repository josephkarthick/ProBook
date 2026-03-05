from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.template_engine import render_template
from core.company_utils import get_current_company_id
from models.vendor import Vendor
from models.item import Item

router = APIRouter()


@router.get("/purchase-page")
def purchase_page(request: Request, db: Session = Depends(get_db)):

    company_id = get_current_company_id(request)

    vendors = db.query(Vendor).filter(
        Vendor.company_id == company_id,
        Vendor.is_active == True
    ).all()

    items = db.query(Item).filter(
        Item.company_id == company_id,
        Item.is_active == True
    ).all()

    return render_template(
        "ProBook/Purchase/purchase.html",
        request,
        {
            "vendors": vendors,
            "items": items
        }
    )