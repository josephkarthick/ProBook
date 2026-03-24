from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/delivery", tags=["Delivery UI"])


@router.get("/")
def delivery_page(request: Request):
    return templates.TemplateResponse(
        "sales/delivery.html",
        {"request": request}
    )