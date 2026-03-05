from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.template_engine import render_template
from models.vendor import Vendor

router = APIRouter()


@router.get("/vendors-page")
def vendor_page(request: Request, db: Session = Depends(get_db)):

    company_id = request.session.get("company_id")

    vendors = db.query(Vendor)\
        .filter(Vendor.company_id == company_id)\
        .filter(Vendor.is_active == True)\
        .order_by(Vendor.name)\
        .all()

    return render_template(
        "ProBook/Vendors/vendors.html",
        request,
        {
            "vendors": vendors
        }
    )