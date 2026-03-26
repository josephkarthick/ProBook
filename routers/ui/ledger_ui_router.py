from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter(prefix="/accounting", tags=["Accounting"])

# ==========================
# Ledger Page
# ==========================
@router.get("/ledger", response_class=HTMLResponse)
def ledger_page(request: Request):

    return render_template(
        "ProBook/Accounts/ledger.html",
        request
    )