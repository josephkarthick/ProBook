from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.item import Item
from models.purchase_order import PurchaseOrder
from models.purchase_order_item import PurchaseOrderItem
from models.goods_receipt import GoodsReceipt
from models.goods_receipt_item import GoodsReceiptItem

from schemas.purchase_order_schema import PurchaseOrderCreate
from services.purchase_order_service import create_purchase_order


router = APIRouter(prefix="/api/purchase-orders", tags=["Purchase Orders"])


# CREATE PO
@router.post("/")
def create_po(data: PurchaseOrderCreate, db: Session = Depends(get_db)):

    po = create_purchase_order(db, data)

    return {
        "message": "PO Created",
        "po_id": po.id,
        "po_number": po.po_number
    }


# LIST PO
@router.get("/")
def list_po(db: Session = Depends(get_db)):

    pos = db.query(PurchaseOrder).all()

    result = []

    for po in pos:

        ordered = db.query(
            func.coalesce(func.sum(PurchaseOrderItem.quantity), 0)
        ).filter(
            PurchaseOrderItem.po_id == po.id
        ).scalar()

        received = db.query(
            func.coalesce(func.sum(GoodsReceiptItem.qty_received), 0)
        )\
        .join(GoodsReceipt, GoodsReceipt.id == GoodsReceiptItem.grn_id)\
        .filter(GoodsReceipt.po_id == po.id)\
        .scalar()

        pending = ordered - received

        status = "CLOSED" if pending <= 0 else "PARTIAL"

        result.append({
            "id": po.id,
            "po_number": po.po_number,
            "vendor_id": po.vendor_id,
            "po_date": po.po_date,
            "total_amount": float(po.total_amount),
            "ordered_qty": float(ordered),
            "received_qty": float(received),
            "pending_qty": float(pending),
            "status": status
        })

    return result


# GET SINGLE PO
@router.get("/{po_id}")
def get_po(po_id: int, db: Session = Depends(get_db)):

    po = db.query(PurchaseOrder)\
        .filter(PurchaseOrder.id == po_id)\
        .first()

    if not po:
        return {"detail": "PO not found"}

    items = db.query(PurchaseOrderItem, Item)\
        .join(Item, PurchaseOrderItem.item_id == Item.id)\
        .filter(PurchaseOrderItem.po_id == po_id)\
        .all()

    result_items = []

    for row in items:

        ordered = float(row.PurchaseOrderItem.quantity)

        received = db.query(
            func.coalesce(func.sum(GoodsReceiptItem.qty_received), 0)
        )\
        .join(GoodsReceipt, GoodsReceipt.id == GoodsReceiptItem.grn_id)\
        .filter(
            GoodsReceipt.po_id == po_id,
            GoodsReceiptItem.item_id == row.PurchaseOrderItem.item_id
        )\
        .scalar()

        received = float(received)

        pending = ordered - received

        result_items.append({
            "item_id": row.PurchaseOrderItem.item_id,
            "item_name": row.Item.name,
            "ordered_qty": ordered,
            "received_qty": received,
            "pending_qty": pending,
            "price": float(row.PurchaseOrderItem.price),
            "gst_rate": float(row.PurchaseOrderItem.gst_rate)
        })

    return {
        "id": po.id,
        "po_number": po.po_number,
        "vendor_id": po.vendor_id,
        "po_date": po.po_date,
        "total_amount": float(po.total_amount),
        "status": po.status,
        "items": result_items
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

    # Remove old items
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
    
    
