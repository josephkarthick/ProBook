from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter(prefix="/purchase-orders")


# ==========================
# Purchase Order List Page
# ==========================
@router.get("/list", response_class=HTMLResponse)
def purchase_order_list_page(request: Request):

    return render_template(
        "ProBook/Purchase/po_list.html",
        request
    )


# ==========================
# Create Purchase Order Page
# ==========================
@router.get("/create", response_class=HTMLResponse)
def purchase_order_create_page(request: Request):

    return render_template(
        "ProBook/Purchase/po_create.html",
        request
    )


# ==========================
# Purchase Order View Page
# ==========================
@router.get("/view/{po_id}", response_class=HTMLResponse)
def purchase_order_view_page(request: Request, po_id: int):

    return render_template(
        "ProBook/Purchase/po_view.html",
        request,
        {"po_id": po_id}
    )