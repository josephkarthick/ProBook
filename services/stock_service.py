from models.stock_layer import StockLayer
from models.stock_movement import StockMovement
from sqlalchemy.orm import Session
from decimal import Decimal

from models.stock_movement import StockMovement

def add_stock_purchase(db, company_id, purchase_id, item_id, qty, cost):

    # FIFO Layer
    layer = StockLayer(
        company_id=company_id,
        item_id=item_id,
        qty=qty,
        cost=cost,
        reference_id=purchase_id
    )

    db.add(layer)

    # Movement log
    movement = StockMovement(
        company_id=company_id,
        item_id=item_id,
        qty=qty,
        movement_type="PURCHASE",
        reference_id=purchase_id
    )

    db.add(movement)
    

def reduce_stock_sale(
    db: Session,
    company_id: int,
    ref_id: int,
    item_id: int,
    qty: Decimal
):

    move = StockMove(

        company_id=company_id,

        item_id=item_id,

        qty_in=0,

        qty_out=qty,

        ref_type="SALE",

        ref_id=ref_id

    )

    db.add(move)

    db.flush()    