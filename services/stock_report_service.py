from sqlalchemy.orm import Session
from sqlalchemy import func

from models.stock_layer import StockLayer
from models.item import Item


def get_stock_summary(db: Session, company_id: int):

    rows = db.query(
        Item.id,
        Item.name,
        func.sum(StockLayer.qty).label("qty"),
        func.sum(StockLayer.qty * StockLayer.cost).label("value")
    ).join(
        StockLayer, StockLayer.item_id == Item.id
    ).filter(
        Item.company_id == company_id
    ).group_by(
        Item.id, Item.name
    ).all()

    result = []

    for r in rows:

        result.append({
            "item_id": r.id,
            "item_name": r.name,
            "qty": float(r.qty or 0),
            "value": float(r.value or 0)
        })

    return result