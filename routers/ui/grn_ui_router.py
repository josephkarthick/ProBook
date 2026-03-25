from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter(
    prefix="/purchase",
    tags=["Purchase UI"]
)


# ==========================
# GRN (GOODS RECEIVED)
# ==========================

# LIST
@router.get("/grn", response_class=HTMLResponse)
def grn_list_page(request: Request):
    return render_template(
        "ProBook/Purchase/grn_list.html",
        request
    )


# CREATE
@router.get("/grn/create", response_class=HTMLResponse)
def grn_create_page(request: Request):
    return render_template(
        "ProBook/Purchase/grn_create.html",
        request
    )