from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import get_db
from core.template_engine import render_template
from models.vendor import Vendor

router = APIRouter()


# ==========================
# Vendor List Page
# ==========================
@router.get("/vendors/list", response_class=HTMLResponse)
def vendor_list_page(
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = request.session.get("company_id")

    vendors = db.query(Vendor)\
        .filter(Vendor.company_id == company_id)\
        .all()

    return render_template(
        "ProBook/Vendors/vendors.html",
        request,
        {
            "vendors": vendors
        }
    )


# ==========================
# Add Vendor Page
# ==========================
@router.get("/vendors/add", response_class=HTMLResponse)
def vendor_add_page(request: Request):

    return render_template(
        "ProBook/Vendors/vendor_add.html",
        request
    )