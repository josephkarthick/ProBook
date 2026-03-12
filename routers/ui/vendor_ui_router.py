from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter()


# ==========================
# Vendor List Page
# ==========================
@router.get("/vendors/list", response_class=HTMLResponse)
def vendor_list_page(request: Request):

    return render_template(
        "ProBook/Vendors/vendors.html",
        request
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