from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from models.item_category import ItemCategory
from core.company_utils import get_current_company_id

router = APIRouter(prefix="/item-categories", tags=["Item Categories"])


@router.post("/")
def create_category(name: str, parent_id: int | None, request: Request, db: Session = Depends(get_db)):

    company_id = get_current_company_id(request)

    cat = ItemCategory(
        company_id=company_id,
        name=name,
        parent_id=parent_id
    )

    db.add(cat)
    db.commit()
    db.refresh(cat)

    return cat


@router.get("/")
def list_categories(request: Request, db: Session = Depends(get_db)):

    company_id = get_current_company_id(request)

    return db.query(ItemCategory)\
        .filter(ItemCategory.company_id == company_id)\
        .all()