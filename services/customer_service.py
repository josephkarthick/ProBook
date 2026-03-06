from models.customer import Customer
from models.accounts import Account


def create_customer(db, data, company_id):

    customer = Customer(
        company_id=company_id,
        name=data.name,
        phone=data.phone,
        email=data.email,
        address=data.address,
        gst_number=data.gst_number
    )

    db.add(customer)
    db.flush()

    # Create receivable ledger account
    account = Account(
        company_id=company_id,
        name=f"Accounts Receivable - {customer.name}",
        account_type="ASSET",
        is_group=False,
        customer_id=customer.id
    )

    db.add(account)

    db.commit()

    return customer