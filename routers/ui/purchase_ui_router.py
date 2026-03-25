from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter(prefix="/purchase", tags=["Purchase UI"])


# ==========================
# PURCHASE ORDER (PO)
# ==========================

# LIST
@router.get("/order", response_class=HTMLResponse)
def po_list_page(request: Request):
    return render_template(
        "ProBook/Purchase/po_list.html",
        request
    )


# CREATE
@router.get("/order/create", response_class=HTMLResponse)
def po_create_page(request: Request):
    return render_template(
        "ProBook/Purchase/po_create.html",
        request
    )


# VIEW
@router.get("/order/{po_id}", response_class=HTMLResponse)
def view_po_page(request: Request, po_id: int):
    return render_template(
        "ProBook/Purchase/po_view.html",
        request,
        {"po_id": po_id}
    )


# EDIT
@router.get("/order/{po_id}/edit", response_class=HTMLResponse)
def edit_po_page(request: Request, po_id: int):
    return render_template(
        "ProBook/Purchase/po_create.html",
        request,
        {
            "po_id": po_id,
            "mode": "edit"
        }
    )




# ==========================
# PURCHASE BILL
# ==========================

# LIST
@router.get("/bill", response_class=HTMLResponse)
def purchase_list_page(request: Request):
    return render_template(
        "ProBook/Purchase/purchase_list.html",
        request
    )


# CREATE
@router.get("/bill/create", response_class=HTMLResponse)
def purchase_create_page(request: Request):
    return render_template(
        "ProBook/Purchase/purchase_bill.html",
        request
    )