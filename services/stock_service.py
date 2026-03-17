from sqlalchemy.orm import Session
from decimal import Decimal
from fastapi import HTTPException
from models.item import Item
from models.stock_layer import StockLayer
from models.stock_movement import StockMovement


# ===============================
# ADD STOCK FROM PURCHASE
# ===============================

def add_stock_purchase(db: Session, company_id, purchase_id, item_id, qty, cost):

    # Validate item exists
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.company_id == company_id,
        Item.is_active == True
    ).first()

    if not item:
        raise Exception(f"Item {item_id} does not exist")

    qty = Decimal(qty)
    cost = Decimal(cost)

    # FIFO stock layer
    layer = StockLayer(
        company_id=company_id,
        item_id=item_id,
        qty=qty,
        cost=cost,
        reference_id=int(purchase_id)
    )

    db.add(layer)

    # Movement log
    movement = StockMovement(
        company_id=company_id,
        item_id=item_id,
        qty=qty,
        movement_type="PURCHASE",
        reference_id=int(purchase_id)
    )

    db.add(movement)

    db.commit()


# ===============================
# REDUCE STOCK FROM SALE
# ===============================


def reduce_stock_sale(db, company_id, item_id, qty, reference_id):

    qty = Decimal(qty)

    item = db.query(Item).filter(
        Item.id == item_id,
        Item.company_id == company_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found for company {company_id}"
        )

    # check stock availability
    validate_stock_before_sale(db, company_id, item_id, qty)

    movement = StockMovement(
        company_id=company_id,
        item_id=item_id,
        qty=-qty,
        movement_type="SALE",
        reference_id=int(reference_id)
    )

    db.add(movement)
    db.commit()


# ===============================
# GET CURRENT STOCK
# ===============================

def get_item_stock(db: Session, company_id, item_id):

    from sqlalchemy import func

    stock = db.query(
        func.coalesce(func.sum(StockMovement.qty), 0)
    ).filter(
        StockMovement.company_id == company_id,
        StockMovement.item_id == item_id
    ).scalar()

    return stock


# ===============================
# CHECK STOCK BEFORE SALE
# ===============================

def validate_stock_before_sale(db: Session, company_id, item_id, qty):

    current_stock = get_item_stock(db, company_id, item_id)

    if current_stock < qty:
        raise Exception(
            f"Insufficient stock. Available: {current_stock}, Required: {qty}"
        )

    return True
    

def stock_adjustment(db: Session, company_id, item_id, qty, adjustment_type, reason=None):

    qty = Decimal(qty)

    item = db.query(Item).filter(
        Item.id == item_id,
        Item.company_id == company_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if adjustment_type == "OUT":
        validate_stock_before_sale(db, company_id, item_id, qty)
        movement_qty = -qty

    else:
        movement_qty = qty

    # ✅ Movement
    movement = StockMovement(
        company_id=company_id,
        item_id=item_id,
        qty=movement_qty,
        movement_type=f"ADJUSTMENT_{adjustment_type}",
        reference_id=None
    )

    db.add(movement)

    # ✅ Only for IN → add layer
    if adjustment_type == "IN":

        # get avg cost
        avg_cost = get_avg_cost(db, company_id, item_id)

        layer = StockLayer(
            company_id=company_id,
            item_id=item_id,
            qty=qty,
            cost=avg_cost,
            reference_id=None
        )

        db.add(layer)

    db.commit()

    return {"message": "Stock adjusted successfully"}

def get_avg_cost(db: Session, company_id, item_id):

    layers = db.query(
        func.coalesce(func.sum(StockLayer.qty), 0),
        func.coalesce(func.sum(StockLayer.qty * StockLayer.cost), 0)
    ).filter(
        StockLayer.company_id == company_id,
        StockLayer.item_id == item_id
    ).first()

    total_qty = float(layers[0] or 0)
    total_value = float(layers[1] or 0)

    if total_qty == 0:
        return 0

    return total_value / total_qty    