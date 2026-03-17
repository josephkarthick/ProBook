from sqlalchemy.orm import Session
from decimal import Decimal

from models.sales_invoice import SalesInvoice
from models.sales_invoice_item import SalesInvoiceItem

from services.stock_service import reduce_stock_sale
from services.journal_service import create_sales_journal


# ===============================
# GENERATE INVOICE NUMBER
# ===============================
def generate_invoice_no(db, company_id):

    last = db.query(SalesInvoice)\
        .filter(SalesInvoice.company_id == company_id)\
        .order_by(SalesInvoice.id.desc())\
        .first()

    if not last:
        return "SI-00001"

    number = int(last.invoice_no.split("-")[1]) + 1

    return f"SI-{number:05d}"


# ===============================
# CREATE SALES INVOICE
# ===============================
def create_sales_invoice(db: Session, data, company_id):

    invoice_no = generate_invoice_no(db, company_id)

    # ✅ FIX: extract from request
    customer_id = data.customer_id
    invoice_date = data.invoice_date

    total_amount = Decimal("0")
    tax_amount = Decimal("0")

    # ✅ CREATE EMPTY INVOICE FIRST
    invoice = SalesInvoice(
        company_id=company_id,
        customer_id=customer_id,
        invoice_no=invoice_no,
        invoice_date=invoice_date,

        total_amount=0,
        tax_amount=0,
        grand_total=0,

        paid_amount=0,
        balance_amount = grand_total,
        payment_status="UNPAID"
    )

    db.add(invoice)
    db.flush()   # get invoice.id

    # ===============================
    # ADD ITEMS
    # ===============================
    for item in data.items:

        qty = Decimal(str(item.quantity))
        price = Decimal(str(item.price))
        gst_rate = Decimal(str(item.gst_rate))

        subtotal = qty * price
        tax = (subtotal * gst_rate) / Decimal("100")
        total = subtotal + tax

        invoice_item = SalesInvoiceItem(
            invoice_id=invoice.id,
            item_id=item.item_id,
            qty=qty,
            price=price,
            amount=subtotal,
            gst_rate=gst_rate,
            gst_amount=tax,
            total=total
        )

        db.add(invoice_item)

        # 🔥 STOCK REDUCTION
        reduce_stock_sale(
            db,
            company_id,
            item.item_id,
            item.quantity,
            invoice.id
        )

        total_amount += subtotal
        tax_amount += tax

    # ===============================
    # FINAL TOTALS
    # ===============================
    grand_total = total_amount + tax_amount

    invoice.total_amount = total_amount
    invoice.tax_amount = tax_amount
    invoice.grand_total = grand_total

    # ===============================
    # PAYMENT INIT
    # ===============================
    invoice.paid_amount = Decimal("0")
    invoice.balance_amount = grand_total
    invoice.payment_status = "UNPAID"

    db.commit()
    db.refresh(invoice)

    # 🔥 ACCOUNTING ENTRY
    create_sales_journal(db, invoice)

    return invoice