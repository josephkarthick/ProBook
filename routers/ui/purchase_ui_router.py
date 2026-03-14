from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter()


# Purchase Bill Page
from core.template_engine import render_template

@router.get("/purchase/create")
def purchase_create_page(request: Request):

    return render_template(
        "ProBook/Purchase/purchase_bill.html",
        request
    )


# Purchase List Page (optional for later)
@router.get("/purchase/bills", response_class=HTMLResponse)
def purchase_list_page(request: Request):

    return render_template(
        "ProBook/Purchase/purchase_list.html",
        request
    )

@router.get("/purchase/po/view/{po_id}", response_class=HTMLResponse)
def view_po_page(request: Request, po_id: int):

    return render_template(
        "ProBook/Purchase/po_view.html",
        request,
        {"po_id": po_id}
    )

@router.get("/purchase/po/edit/{po_id}", response_class=HTMLResponse)
def edit_po_page(request: Request, po_id: int):

    return render_template(
        "ProBook/Purchase/po_edit.html",
        request,
        {"po_id": po_id}
    )   