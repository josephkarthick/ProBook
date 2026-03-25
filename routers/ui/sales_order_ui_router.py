from fastapi import APIRouter, Request

from core.template_engine import render_template

router = APIRouter(tags=["Sales Order UI"])


def _render_sales_order_page(request: Request):
    return render_template(
        "ProBook/Sales/sales_create.html",
        request
    )


@router.get("/sales-order")
@router.get("/sales-order/", include_in_schema=False)
def sales_order_page(request: Request):
    return _render_sales_order_page(request)


@router.get("/sales/orders", include_in_schema=False)
def sales_order_orders_alias(request: Request):
    return _render_sales_order_page(request)


@router.get("/sales_order_page", include_in_schema=False)
def sales_order_flat_alias(request: Request):
    return _render_sales_order_page(request)
