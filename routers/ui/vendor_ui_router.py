
from fastapi.responses import HTMLResponse
from core.template_engine import render_template
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.company_utils import get_current_company_id

from services.vendor_service import list_vendors

router = APIRouter()


@router.get("/vendors/list", response_class=HTMLResponse)
def vendor_list_page(
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    vendors = list_vendors(db, company_id)

    return render_template(
        "ProBook/Vendors/vendors.html",
        request,
        {
            "vendors": vendors   # ✅ THIS WAS MISSING
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