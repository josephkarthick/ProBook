from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter(tags=["Customer UI"])


# Customer List Page
@router.get("/customers")
def customers_page(request: Request):
    return render_template(
        "ProBook/Contacts/customer_list.html",
        request
    )


# Create Page
@router.get("/customer-create")
def customer_create_page(request: Request):
    return render_template(
        "ProBook/Contacts/customer_create.html",
        request
    )


# Edit Page
@router.get("/customer-edit/{customer_id}")
def customer_edit_page(request: Request, customer_id: int):

    return render_template(
        "ProBook/Contacts/customer_edit.html",
        request,
        {"customer_id": customer_id}
    )