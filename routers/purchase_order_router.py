from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from schemas.purchase_order_schema import PurchaseOrderCreate
from services.purchase_order_service import create_purchase_order

from models.purchase_order import PurchaseOrder
from models.purchase_order_item import PurchaseOrderItem

router = APIRouter(prefix="/api/purchase-orders", tags=["Purchase Orders"])


# CREATE PO
@router.post("/")
def create_po(data: PurchaseOrderCreate, db: Session = Depends(get_db)):
    return create_purchase_order(db, data)


# LIST PO
@router.get("/")
def list_po(db: Session = Depends(get_db)):
    return db.query(PurchaseOrder).all()


# GET SINGLE PO
@router.get("/{po_id}")
def get_po(po_id: int, db: Session = Depends(get_db)):

    po = db.query(PurchaseOrder)\
        .filter(PurchaseOrder.id == po_id)\
        .first()

    if not po:
        return {"detail": "PO not found"}

    items = db.query(PurchaseOrderItem)\
        .filter(PurchaseOrderItem.po_id == po_id)\
        .all()

    return {
        "id": po.id,
        "po_number": po.po_number,
        "vendor_id": po.vendor_id,
        "po_date": po.po_date,
        "total_amount": float(po.total_amount),
        "status": po.status,
        "items": [
            {
                "item_id": i.item_id,
                "quantity": float(i.quantity),
                "price": float(i.price),
                "gst_rate": float(i.gst_rate)
            }
            for i in items
        ]
    }


# UPDATE PO
@router.put("/{po_id}")
def update_po(po_id: int, data: PurchaseOrderCreate,
              db: Session = Depends(get_db)):

    po = db.query(PurchaseOrder)\
        .filter(PurchaseOrder.id == po_id)\
        .first()

    if not po:
        return {"detail": "PO not found"}

    po.vendor_id = data.vendor_id
    po.po_date = data.po_date

    # remove old items
    db.query(PurchaseOrderItem)\
        .filter(PurchaseOrderItem.po_id == po_id)\
        .delete()

    subtotal = 0
    tax_total = 0

    for item in data.items:

        sub = item.quantity * item.price
        tax = sub * item.gst_rate / 100
        total = sub + tax

        subtotal += sub
        tax_total += tax

        new_item = PurchaseOrderItem(
            po_id=po_id,
            item_id=item.item_id,
            quantity=item.quantity,
            price=item.price,
            gst_rate=item.gst_rate,
            total=total
        )

        db.add(new_item)

    po.total_amount = subtotal + tax_total

    db.commit()

    return {"message": "PO Updated"}