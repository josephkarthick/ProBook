from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter(prefix="/accounting", tags=["Accounting"])

# ==========================
# Balance Sheet
# ==========================
@router.get("/balance-sheet", response_class=HTMLResponse)
def balance_sheet_page(request: Request):

    return render_template(
        "ProBook/Accounts/balance_sheet.html",
        request
    )