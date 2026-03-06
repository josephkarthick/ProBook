from models.stock_layer import StockLayer
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