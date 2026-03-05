from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter()

@router.get("/ledger")
def ledger_page(request: Request):

    return render_template(
        "ProBook/Accounts/ledger.html",
        request
    )