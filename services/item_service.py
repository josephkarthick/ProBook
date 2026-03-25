from sqlalchemy.orm import Session
from models.item import Item
from schemas.item_schema import ItemCreate, ItemUpdate
from models.item_category import ItemCategory 
from sqlalchemy import func
from models.stock_movement import StockMovement


def generate_item_code(db, company_id):

    last = db.query(Item)\
        .filter(Item.company_id == company_id)\
        .order_by(Item.id.desc())\
        .first()

    if not last or not last.item_code:
        return "ITM-00001"

    try:
        parts = last.item_code.split("-")

        if len(parts) < 2:
            return "ITM-00001"

        number = int(parts[1]) + 1
        return f"ITM-{number:05d}"

    except Exception:
        return "ITM-00001"


def create_item(db: Session, data: ItemCreate, company_id: int):

    item_code = generate_item_code(db, company_id)

    item = Item(
        company_id=company_id,
        item_code=item_code,
        name=data.name,
        category_id=data.category_id,
        unit=data.unit,
        hsn_code=data.hsn_code,
        gst_rate=data.gst_rate,
        purchase_price=data.purchase_price,
        selling_price=data.selling_price,
        track_inventory=data.track_inventory,
        min_stock_level=data.min_stock_level or 0
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def list_items(db, company_id):

    items = db.query(
        Item.id,
        Item.item_code,
        Item.name,
        Item.unit,
        Item.purchase_price,
        Item.selling_price,
        Item.gst_rate,
        Item.min_stock_level,
        ItemCategory.name.label("category_name"),  # ✅ FIXED

        func.coalesce(func.sum(StockMovement.qty), 0).label("stock")

    ).outerjoin(
        StockMovement,
        (StockMovement.item_id == Item.id) &
        (StockMovement.company_id == company_id)

    ).outerjoin(   # ✅ FIXED BRACKET
        ItemCategory,
        ItemCategory.id == Item.category_id

    ).filter(
        Item.company_id == company_id,
        Item.is_active == True

    ).group_by(
        Item.id,
        Item.item_code,
        Item.name,
        Item.unit,
        Item.purchase_price,
        Item.selling_price,
        Item.gst_rate,
        Item.min_stock_level,
        ItemCategory.name   # ✅ FIXED

    ).all()

    return [
        {
            "id": i.id,
            "item_code": i.item_code,
            "name": i.name,
            "unit": i.unit,
            "purchase_price": float(i.purchase_price or 0),
            "selling_price": float(i.selling_price or 0),
            "gst_rate": float(i.gst_rate or 0),
            "min_stock_level": float(i.min_stock_level or 0),
            "stock": float(i.stock or 0),
            "category_name": i.category_name or ""
        }
        for i in items
    ]

def update_item(db: Session, item_id: int, data: ItemUpdate, company_id: int):

    item = db.query(Item).filter(
        Item.id == item_id,
        Item.company_id == company_id,
        Item.is_active == True
    ).first()

    if not item:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item

def delete_item(db: Session, item_id: int, company_id: int):

    item = db.query(Item).filter(
        Item.id == item_id,
        Item.company_id == company_id,
        Item.is_active == True
    ).first()

    if not item:
        return None

    item.is_active = False
    db.commit()

    return item


    