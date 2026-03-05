from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.template_engine import render_template
from core.company_utils import get_current_company_id
from models.item import Item

router = APIRouter()


@router.get("/item-page")
def item_page(request: Request, db: Session = Depends(get_db)):

    company_id = get_current_company_id(request)

    items = (
        db.query(Item)
        .filter(Item.company_id == company_id)
        .filter(Item.is_active == True)
        .all()
    )

    return render_template(
        "ProBook/Items/items.html",
        request,
        {
            "items": items
        }
    )