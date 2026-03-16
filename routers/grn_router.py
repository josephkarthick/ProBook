from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from services.grn_service import create_grn

from models.goods_receipt import GoodsReceipt
from models.goods_receipt_item import GoodsReceiptItem
from models.purchase_order import PurchaseOrder
from models.purchase_order_item import PurchaseOrderItem
from models.vendor import Vendor
from models.item import Item

from schemas.grn_schema import GRNCreate


router = APIRouter(prefix="/api/grn", tags=["GRN"])


# CREATE GRN
@router.post("/")
def create_goods_receipt(data: GRNCreate, db: Session = Depends(get_db)):
    return create_grn(db, data.model_dump())


@router.get("/")
def list_grn(db: Session = Depends(get_db)):

    grns = db.query(
        GoodsReceipt.id,
        GoodsReceipt.grn_no,
        GoodsReceipt.receipt_date,
        GoodsReceipt.status,
        GoodsReceipt.po_id,
        PurchaseOrder.po_number,
        Vendor.name.label("vendor_name")
    )\
    .join(PurchaseOrder, GoodsReceipt.po_id == PurchaseOrder.id)\
    .join(Vendor, GoodsReceipt.vendor_id == Vendor.id)\
    .order_by(GoodsReceipt.id.asc())\
    .all()

    result = []

    for g in grns:

        # Ordered Qty
        ordered = db.query(
            func.coalesce(func.sum(PurchaseOrderItem.quantity), 0)
        ).filter(
            PurchaseOrderItem.po_id == g.po_id
        ).scalar()

        # Received in THIS GRN
        received = db.query(
            func.coalesce(func.sum(GoodsReceiptItem.qty_received), 0)
        ).filter(
            GoodsReceiptItem.grn_id == g.id
        ).scalar()

        # Total received before this GRN
        received_before = db.query(
            func.coalesce(func.sum(GoodsReceiptItem.qty_received), 0)
        )\
        .join(GoodsReceipt, GoodsReceipt.id == GoodsReceiptItem.grn_id)\
        .filter(
            GoodsReceipt.po_id == g.po_id,
            GoodsReceipt.id < g.id
        ).scalar()

        pending = ordered - (received_before + received)

        result.append({
            "grn_no": g.grn_no,
            "po_number": g.po_number,
            "vendor_name": g.vendor_name,
            "receipt_date": g.receipt_date.strftime("%Y-%m-%d"),
            "ordered_qty": float(ordered),
            "received_qty": float(received),
            "pending_qty": float(pending),
            "status": g.status
        })

    return result


# GET PO ITEMS FOR GRN
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

        received = float(received or 0)

        pending = ordered - received

        result_items.append({
            "item_id": row.PurchaseOrderItem.item_id,
            "item_name": row.Item.name,
            "ordered_qty": ordered,
            "received_qty": received,
            "pending_qty": pending
        })

    return {
        "po_id": po.id,
        "items": result_items
    }
    
