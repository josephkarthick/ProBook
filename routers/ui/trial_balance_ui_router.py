from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter(prefix="/accounting", tags=["Accounting"])


# ==========================
# Trial Balance
# ==========================
@router.get("/trial-balance", response_class=HTMLResponse)
def trial_balance_page(request: Request):

    return render_template(
        "ProBook/Accounts/trial_balance.html",
        request
    )
