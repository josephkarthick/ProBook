from sqlalchemy.orm import Session
from decimal import Decimal

from models.sales_invoice import SalesInvoice
from models.sales_invoice_item import SalesInvoiceItem

from services.stock_service import reduce_stock_sale
from services.journal_service import create_sales_journal



def generate_invoice_no(db, company_id):

    last = db.query(SalesInvoice)\
        .filter(SalesInvoice.company_id == company_id)\
        .order_by(SalesInvoice.id.desc())\
        .first()

    if not last:
        return "SI-00001"

    number = int(last.invoice_no.split("-")[1]) + 1

    return f"SI-{number:05d}"


def create_sales_invoice(db: Session, data, company_id):

    invoice_no = generate_invoice_no(db, company_id)

    total_amount = Decimal("0")
    tax_amount = Decimal("0")

    invoice = SalesInvoice(
        company_id=company_id,
        customer_id=data.customer_id,
        invoice_no=invoice_no,
        invoice_date=data.invoice_date
    )

    db.add(invoice)
    db.flush()

    for item in data.items:

        qty = Decimal(item.quantity)
        price = Decimal(item.price)
        gst = Decimal(item.gst_rate)

        subtotal = qty * price
        tax = subtotal * gst / Decimal("100")
        total = subtotal + tax

        invoice_item = SalesInvoiceItem(
            invoice_id=invoice.id,
            item_id=item.item_id,
            qty=qty,
            price=price,
            amount=subtotal,
            gst_rate=gst,
            gst_amount=tax,
            total=total
        )

        db.add(invoice_item)

        reduce_stock_sale(
            db,
            company_id,
            item.item_id,
            qty,
            invoice.id
        )

        total_amount += subtotal
        tax_amount += tax

    invoice.total_amount = total_amount
    invoice.tax_amount = tax_amount
    invoice.grand_total = total_amount + tax_amount

    db.commit()
    db.refresh(invoice)

    create_sales_journal(db, invoice)

    return invoice