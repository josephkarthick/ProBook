from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter()

@router.get("/trial-balance")
def trial_balance_page(request: Request):

    return render_template(
        "ProBook/Accounts/trial_balance.html",
        request
    )