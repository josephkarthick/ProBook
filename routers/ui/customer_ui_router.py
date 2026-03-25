from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter(
    prefix="/customers",
    tags=["Customer UI"]
)


# ===============================
# CUSTOMER LIST
# ===============================
@router.get("/list")
def customers_page(request: Request):
    return render_template(
        "ProBook/Contacts/customer_list.html",
        request
    )


# ===============================
# CUSTOMER CREATE
# ===============================
@router.get("/create")
def customer_create_page(request: Request):
    return render_template(
        "ProBook/Contacts/customer_create.html",
        request
    )


# ===============================
# CUSTOMER EDIT
# ===============================
@router.get("/{customer_id}/edit")
def customer_edit_page(request: Request, customer_id: int):
    return render_template(
        "ProBook/Contacts/customer_edit.html",
        request,
        {"customer_id": customer_id}
    )