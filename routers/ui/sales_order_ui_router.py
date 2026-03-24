from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/sales-order", tags=["Sales Order UI"])


@router.get("/")
def sales_order_page(request: Request):
    return templates.TemplateResponse(
        "sales/sales_order.html",
        {"request": request}
    )