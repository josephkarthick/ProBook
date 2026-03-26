from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter(prefix="/accounting", tags=["Accounting"])

# ==========================
# Journal Page
# ==========================
@router.get("/journal", response_class=HTMLResponse)
def journals_page(request: Request):

    return render_template(
        "ProBook/Accounts/journals.html",
        request
    )