@router.get("/{customer_id}/ledger")
def customer_ledger(customer_id: int, db: Session = Depends(get_db)):

    account = db.query(Account)\
        .filter(Account.customer_id == customer_id)\
        .first()

    if not account:
        return []

    rows = db.query(JournalLine)\
        .filter(JournalLine.account_id == account.id)\
        .all()

    return rows