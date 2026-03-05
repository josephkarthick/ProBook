from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from core.company_utils import get_current_company_id

from schemas.item_schema import ItemCreate, ItemUpdate
from services.item_service import (
    create_item,
    list_items,
    update_item,
    delete_item
)

router = APIRouter(prefix="/api/items", tags=["Items"])


@router.post("")
def create_item_api(
    data: ItemCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    company_id = get_current_company_id(request)
    return create_item(db, data, company_id)


@router.get("")
def list_items_api(
    request: Request,
    db: Session = Depends(get_db)
):
    company_id = get_current_company_id(request)
    return list_items(db, company_id)


@router.put("/{item_id}")
def update_item_api(
    item_id: int,
    data: ItemUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    company_id = get_current_company_id(request)

    item = update_item(db, item_id, data, company_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.delete("/{item_id}")
def delete_item_api(
    item_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    company_id = get_current_company_id(request)

    item = delete_item(db, item_id, company_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted"}