from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter(prefix="/accounting", tags=["Accounting"])

# ==========================
# Profit & Loss
# ==========================
@router.get("/profit-loss", response_class=HTMLResponse)
def profit_loss_page(request: Request):

    return render_template(
        "ProBook/Accounts/profit_loss.html",
        request
    )
