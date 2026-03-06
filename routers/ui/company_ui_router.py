from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter()


# ==========================
# COMPANY PAGE
# ==========================
@router.get("/companies", response_class=HTMLResponse)
def companies_page(request: Request):

    return render_template(
        "ProBook/Settings/companies.html",
        request
    )