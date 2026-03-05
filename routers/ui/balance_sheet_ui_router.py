from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter()

@router.get("/balance-sheet")
def balance_sheet_page(request: Request):

    return render_template(
        "ProBook/Accounts/balance_sheet.html",
        request
    )