from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from utils.template_helpers import render_template

router = APIRouter()

@router.get("/settings/companies", response_class=HTMLResponse)
def company_page(request: Request):
    return render_template(
        "VaisKart/Settings/companies.html",
        request
    )