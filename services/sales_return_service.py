from sqlalchemy.orm import Session
from decimal import Decimal

from models.sales_return import SalesReturn
from models.sales_return_item import SalesReturnItem

from services.stock_service import add_stock_purchase
from services.journal_service import create_sales_return_journal


def generate_return_no(db, company_id):

    last = db.query(SalesReturn)\
        .filter(SalesReturn.company_id == company_id)\
        .order_by(SalesReturn.id.desc())\
        .first()

    if not last:
        return "SR-00001"

    number = int(last.return_no.split("-")[1]) + 1

    return f"SR-{number:05d}"


def create_sales_return(db: Session, data, company_id):

    return_no = generate_return_no(db, company_id)

    total_amount = Decimal("0")
    tax_amount = Decimal("0")

    sales_return = SalesReturn(
        company_id=company_id,
        invoice_id=data.invoice_id,
        return_no=return_no,
        return_date=data.return_date
    )

    db.add(sales_return)
    db.flush()

    for item in data.items:

        qty = Decimal(item.quantity)
        price = Decimal(item.price)
        gst = Decimal(item.gst_rate)

        subtotal = qty * price
        tax = subtotal * gst / Decimal("100")
        total = subtotal + tax

        return_item = SalesReturnItem(

            return_id=sales_return.id,
            invoice_item_id=item.invoice_item_id,
            item_id=item.item_id,
            qty=qty,
            price=price,
            amount=subtotal,
            gst_rate=gst,
            gst_amount=tax,
            total=total
        )

        db.add(return_item)

        # STOCK INCREASE
        add_stock_purchase(
            db,
            company_id,
            sales_return.id,
            item.item_id,
            qty,
            price
        )

        total_amount += subtotal
        tax_amount += tax

    sales_return.total_amount = total_amount
    sales_return.tax_amount = tax_amount
    sales_return.grand_total = total_amount + tax_amount

    db.commit()
    db.refresh(sales_return)

    create_sales_return_journal(db, sales_return)

    return sales_return