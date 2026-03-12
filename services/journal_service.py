from sqlalchemy.orm import Session
from models.journal_entry import JournalEntry
from models.journal_line import JournalLine
from models.accounts import Account
from schemas.journal_schema import JournalEntryCreate
from models.journal_entry import JournalEntry
from models.journal_line import JournalLine
from models.accounts import Account
from datetime import date


def create_sales_journal(db, invoice):

    receivable = db.query(Account).filter(
        Account.name == "Accounts Receivable",
        Account.company_id == invoice.company_id
    ).first()

    sales = db.query(Account).filter(
        Account.name == "Sales",
        Account.company_id == invoice.company_id
    ).first()

    gst = db.query(Account).filter(
        Account.name == "GST Payable",
        Account.company_id == invoice.company_id
    ).first()

    if not receivable or not sales or not gst:
        raise Exception("Required accounts not found")

    journal = JournalEntry(

        company_id=invoice.company_id,
        reference_no=invoice.invoice_no,
        date=invoice.invoice_date,
        narration=f"Sales Invoice {invoice.invoice_no}",
        status="POSTED"
    )

    db.add(journal)
    db.flush()

    # DR Accounts Receivable
    db.add(JournalLine(
        journal_id=journal.id,
        account_id=receivable.id,
        debit=invoice.grand_total,
        credit=0
    ))

    # CR Sales
    db.add(JournalLine(
        journal_id=journal.id,
        account_id=sales.id,
        debit=0,
        credit=invoice.total_amount
    ))

    # CR GST
    if invoice.tax_amount > 0:
        db.add(JournalLine(
            journal_id=journal.id,
            account_id=gst.id,
            debit=0,
            credit=invoice.tax_amount
        ))

    db.commit()

def create_journal(db: Session, data: JournalEntryCreate, company_id: int):

    if len(data.lines) < 2:
        raise ValueError("Journal must have at least 2 lines")

    total_debit = sum(line.debit for line in data.lines)
    total_credit = sum(line.credit for line in data.lines)

    if round(total_debit, 2) != round(total_credit, 2):
        raise ValueError("Debit and Credit must match")

    journal = JournalEntry(
        company_id=company_id,
        reference_no=data.reference_no,
        date=data.date,
        narration=data.narration,
        status="POSTED"
    )

    db.add(journal)
    db.flush()

    for line in data.lines:

        if line.debit > 0 and line.credit > 0:
            raise ValueError("Line cannot have both debit and credit")

        account = db.query(Account).filter(
            Account.id == line.account_id,
            Account.company_id == company_id
        ).first()

        if not account:
            raise ValueError("Invalid account for this company")

        db.add(
            JournalLine(
                journal_id=journal.id,
                account_id=line.account_id,
                debit=line.debit,
                credit=line.credit
            )
        )

    db.commit()
    db.refresh(journal)

    return journal

def create_purchase_journal(db, bill):

    purchase_account = db.query(Account).filter(
        Account.name == "Purchase",
        Account.company_id == bill.company_id
    ).first()

    gst_account = db.query(Account).filter(
        Account.name == "Input GST",
        Account.company_id == bill.company_id
    ).first()

    payable_account = db.query(Account).filter(
        Account.name == "Accounts Payable",
        Account.company_id == bill.company_id
    ).first()

    if not purchase_account or not gst_account or not payable_account:
        raise Exception("Required accounts not found")

    journal = JournalEntry(
        company_id=bill.company_id,
        reference_no=bill.bill_no,
        date=bill.bill_date,
        narration="Purchase Bill",
        status="POSTED"
    )

    db.add(journal)
    db.flush()

    db.add(JournalLine(
        journal_id=journal.id,
        account_id=purchase_account.id,
        debit=bill.total_amount,
        credit=0
    ))

    db.add(JournalLine(
        journal_id=journal.id,
        account_id=gst_account.id,
        debit=bill.tax_amount,
        credit=0
    ))

    db.add(JournalLine(
        journal_id=journal.id,
        account_id=payable_account.id,
        debit=0,
        credit=bill.grand_total
    ))

    db.commit()
    
def create_sales_return_journal(db, sales_return):

    entry = create_journal_entry(
        db,
        company_id=sales_return.company_id,
        date=sales_return.return_date,
        reference=sales_return.return_no,
        narration="Sales Return"
    )

    add_journal_line(db, entry.id, "Sales Return", debit=sales_return.total_amount)

    add_journal_line(db, entry.id, "Output GST", debit=sales_return.tax_amount)

    add_journal_line(
        db,
        entry.id,
        "Accounts Receivable",
        credit=sales_return.grand_total
    )

    db.commit()    
    
    
def create_vendor_payment_journal(db, payment):

    from models.journal_entry import JournalEntry
    from models.journal_line import JournalLine

    entry = JournalEntry(
        company_id=payment.company_id,
        date=payment.payment_date,
        reference=payment.payment_no,
        narration="Vendor Payment"
    )

    db.add(entry)
    db.flush()

    # Debit Accounts Payable
    db.add(JournalLine(
        journal_id=entry.id,
        account_name="Accounts Payable",
        debit=payment.total_amount,
        credit=0
    ))

    # Credit Cash / Bank
    db.add(JournalLine(
        journal_id=entry.id,
        account_name="Cash",
        debit=0,
        credit=payment.total_amount
    ))

    db.commit()    