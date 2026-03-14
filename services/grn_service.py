from sqlalchemy.orm import Session
from models.goods_receipt import GoodsReceipt
from models.goods_receipt_item import GoodsReceiptItem


def create_grn(db: Session, data):

    grn = GoodsReceipt(
        company_id=data["company_id"],
        vendor_id=data["vendor_id"],
        po_id=data.get("po_id"),
        grn_no=data["grn_no"],
        receipt_date=data["receipt_date"]
    )

    db.add(grn)
    db.flush()

    for item in data["items"]:

        grn_item = GoodsReceiptItem(
            grn_id=grn.id,
            item_id=item["item_id"],
            qty_received=item["qty"]
        )

        db.add(grn_item)

    db.commit()

    return grn