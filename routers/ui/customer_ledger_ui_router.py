from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.template_engine import render_template

router = APIRouter()


@router.get("/customers/ledger/{customer_id}", response_class=HTMLResponse)
def customer_ledger_page(request: Request, customer_id: int):

    return render_template(
        "ProBook/Contacts/customer_ledger.html",
        request,
        {
            "customer_id": customer_id
        }
    )