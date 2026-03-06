from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter(tags=["Sales UI"])


@router.get("/sales")
def sales_list_page(request: Request):

    return render_template(
        "ProBook/Sales/sales_list.html",
        request
    )


@router.get("/sales-create")
def sales_create_page(request: Request):

    return render_template(
        "ProBook/Sales/sales_create.html",
        request
    )