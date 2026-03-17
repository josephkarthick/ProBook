from sqlalchemy.orm import Session
from sqlalchemy import func
from models.stock_layer import StockLayer
from models.stock_movement import StockMovement
from models.item import Item


def get_stock_summary(db: Session, company_id: int):

    items = db.query(Item).filter(
        Item.company_id == company_id
    ).all()

    result = []

    for item in items:

        # ✅ STOCK FROM MOVEMENT
        qty = db.query(func.coalesce(func.sum(StockMovement.qty), 0)).filter(
            StockMovement.company_id == company_id,
            StockMovement.item_id == item.id
        ).scalar()

        # ✅ VALUE FROM LAYER
        value = db.query(func.coalesce(func.sum(
            StockLayer.qty * StockLayer.cost
        ), 0)).filter(
            StockLayer.company_id == company_id,
            StockLayer.item_id == item.id
        ).scalar()

        qty = float(qty or 0)
        value = float(value or 0)

        avg_cost = value / qty if qty else 0

        result.append({
            "item_id": item.id,
            "item_name": item.name,
            "qty": qty,
            "avg_cost": avg_cost,
            "stock_value": value,
            "min_stock": float(item.min_stock_level or 0)
        })

    return result
    

def get_low_stock_items(db: Session, company_id: int):

    rows = db.query(
        Item.id,
        Item.name,
        Item.min_stock_level,
        func.coalesce(func.sum(StockMovement.qty), 0).label("stock_qty")
    ).outerjoin(
        StockMovement,
        (StockMovement.item_id == Item.id) &
        (StockMovement.company_id == company_id)
    ).filter(
        Item.company_id == company_id
    ).group_by(
        Item.id, Item.name, Item.min_stock_level
    ).all()

    result = []

    for r in rows:

        current_stock = float(r.stock_qty or 0)
        min_stock = float(r.min_stock_level or 0)

        if current_stock < min_stock:

            result.append({
                "item_id": r.id,
                "item_name": r.name,
                "stock": current_stock,
                "min_stock": min_stock,
                "shortage": min_stock - current_stock
            })

    return result    