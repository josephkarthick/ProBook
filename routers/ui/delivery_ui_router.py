from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter(prefix="/delivery", tags=["Delivery UI"])


# ===============================
# DELIVERY LIST PAGE
# ===============================
@router.get("/list", response_class=HTMLResponse)
def delivery_list_page(request: Request):

    return render_template(
        "ProBook/Sales/delivery_list.html",
        request
    )


# ===============================
# DELIVERY CREATE PAGE
# ===============================
@router.get("/create", response_class=HTMLResponse)
def delivery_create_page(request: Request):

    return render_template(
        "ProBook/Sales/delivery_create.html",
        request
    )