from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter()


# ==========================
# Purchase Order List
# ==========================
@router.get("/purchase/po/list", response_class=HTMLResponse)
def purchase_order_list_page(request: Request):

    return render_template(
        "ProBook/Purchase/po_list.html",
        request
    )


# ==========================
# Create Purchase Order
# ==========================
@router.get("/purchase/po/create", response_class=HTMLResponse)
def purchase_order_create_page(request: Request):

    return render_template(
        "ProBook/Purchase/po_create.html",
        request
    )


# ==========================
# View Purchase Order
# ==========================
@router.get("/purchase/po/view/{po_id}", response_class=HTMLResponse)
def purchase_order_view_page(request: Request, po_id: int):

    return render_template(
        "ProBook/Purchase/po_view.html",
        request,
        {"po_id": po_id}
    )