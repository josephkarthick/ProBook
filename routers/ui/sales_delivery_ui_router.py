from fastapi import APIRouter, Request

from core.template_engine import render_template

router = APIRouter(prefix="/delivery", tags=["Delivery UI"])


@router.get("/")
def delivery_page(request: Request):
    return render_template(
        "ProBook/Sales/delivery.html",
        request
    )
