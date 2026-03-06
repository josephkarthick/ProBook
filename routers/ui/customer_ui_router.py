from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter(tags=["Customer UI"])


@router.get("/customers")
def customers_page(request: Request):

    return render_template(
        "ProBook/Contacts/customer_list.html",
        request
    )


@router.get("/customer-create")
def customer_create_page(request: Request):

    return render_template(
        "ProBook/Contacts/customer_create.html",
        request
    )