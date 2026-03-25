from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter(
    prefix="/purchase",
    tags=["Purchase UI"]
)


# =========================
# PURCHASE PAYMENT LIST
# =========================
@router.get("/payment", response_class=HTMLResponse)
def purchase_payment_page(request: Request):

    return render_template(
        "ProBook/Purchase/purchase_payment.html",
        request
    )