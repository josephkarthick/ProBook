from sqlalchemy.orm import Session
from sqlalchemy import func

from models.goods_receipt import GoodsReceipt
from models.goods_receipt_item import GoodsReceiptItem
from models.purchase_order import PurchaseOrder
from models.purchase_order_item import PurchaseOrderItem
from models.vendor import Vendor


def create_grn(db: Session, data: dict):

    # ------------------------------------------------
    # Get Purchase Order
    # ------------------------------------------------

    po = db.query(PurchaseOrder)\
        .filter(PurchaseOrder.id == data["po_id"])\
        .first()

    if not po:
        raise ValueError("Purchase Order not found")

    # Prevent GRN if PO already closed
    if po.status == "CLOSED":
        raise ValueError("Purchase Order already fully received")


    # ------------------------------------------------
    # Get Vendor
    # ------------------------------------------------

    vendor = db.query(Vendor)\
        .filter(Vendor.id == po.vendor_id)\
        .first()

    if not vendor:
        raise ValueError("Vendor not found")

    company_id = vendor.company_id


    # ------------------------------------------------
    # Generate GRN Number
    # ------------------------------------------------

    last_grn = db.query(GoodsReceipt)\
        .filter(GoodsReceipt.company_id == company_id)\
        .order_by(GoodsReceipt.id.desc())\
        .first()

    next_no = int(last_grn.grn_no.split("-")[1]) + 1 if last_grn else 1

    grn_no = f"GRN-{next_no:05d}"


    try:

        # ------------------------------------------------
        # Create GRN
        # ------------------------------------------------

        grn = GoodsReceipt(
            company_id=company_id,
            vendor_id=vendor.id,
            po_id=po.id,
            grn_no=grn_no,
            receipt_date=data["receipt_date"]
        )

        db.add(grn)
        db.flush()


        # ------------------------------------------------
        # Insert GRN Items
        # ------------------------------------------------

        for item in data["items"]:

            po_item = db.query(PurchaseOrderItem)\
                .filter(
                    PurchaseOrderItem.po_id == po.id,
                    PurchaseOrderItem.item_id == item["item_id"]
                )\
                .first()

            if not po_item:
                raise ValueError("PO item not found")


            # Total already received for this item
            received_qty = db.query(
                func.coalesce(func.sum(GoodsReceiptItem.qty_received), 0)
            )\
            .join(GoodsReceipt, GoodsReceipt.id == GoodsReceiptItem.grn_id)\
            .filter(
                GoodsReceipt.po_id == po.id,
                GoodsReceiptItem.item_id == item["item_id"]
            )\
            .scalar()

            remaining_qty = po_item.quantity - received_qty


            if item["qty"] > remaining_qty:
                raise ValueError(
                    f"Cannot receive more than remaining qty ({remaining_qty})"
                )


            grn_item = GoodsReceiptItem(
                grn_id=grn.id,
                item_id=item["item_id"],
                qty_received=item["qty"]
            )

            db.add(grn_item)


        # ------------------------------------------------
        # Recalculate PO totals
        # ------------------------------------------------

        total_order = db.query(
            func.coalesce(func.sum(PurchaseOrderItem.quantity), 0)
        )\
        .filter(PurchaseOrderItem.po_id == po.id)\
        .scalar()


        total_received = db.query(
            func.coalesce(func.sum(GoodsReceiptItem.qty_received), 0)
        )\
        .join(GoodsReceipt, GoodsReceipt.id == GoodsReceiptItem.grn_id)\
        .filter(GoodsReceipt.po_id == po.id)\
        .scalar()


        # ------------------------------------------------
        # Update PO Status
        # ------------------------------------------------

        if total_received >= total_order:
            po.status = "CLOSED"
        else:
            po.status = "PARTIAL"


        db.commit()

        return {
            "message": "GRN Created Successfully",
            "grn_no": grn_no
        }


    except Exception as e:

        db.rollback()
        raise e