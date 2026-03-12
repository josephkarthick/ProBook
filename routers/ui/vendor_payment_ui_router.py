from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter(tags=["Vendor Payments UI"])


@router.get("/vendor-payments")
def payment_list(request: Request):

    return render_template(
        "ProBook/Purchase/vendor_payment_list.html",
        request
    )


@router.get("/vendor-payment-create")
def payment_create(request: Request):

    return render_template(
        "ProBook/Purchase/vendor_payment_create.html",
        request
    )