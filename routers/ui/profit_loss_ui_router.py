from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter()

@router.get("/profit-loss")
def profit_loss_page(request: Request):

    return render_template(
        "ProBook/Accounts/profit_loss.html",
        request
    )