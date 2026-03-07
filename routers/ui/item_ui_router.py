from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.company_utils import get_current_company_id
from core.template_engine import render_template
from services.item_service import list_items
from services.category_service import list_categories

router = APIRouter()


@router.get("/items")
def items_page(
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    items = list_items(db, company_id)
    categories = list_categories(db, company_id)

    return render_template(
        "ProBook/Items/items.html",
        request,
        {
            "items": items,
            "categories": categories
        }
    )