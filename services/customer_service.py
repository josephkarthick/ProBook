from sqlalchemy.orm import Session
from models.customer import Customer


# CREATE CUSTOMER
def create_customer(db: Session, data, company_id):

    customer = Customer(
        company_id=company_id,
        name=data.name,
        phone=data.phone,
        email=data.email,
        address=data.address,
        gst_number=data.gst_number,
        is_active=True
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


# LIST CUSTOMERS
def list_customers(db: Session, company_id):

    return db.query(Customer)\
        .filter(Customer.company_id == company_id)\
        .filter(Customer.is_active == True)\
        .order_by(Customer.id.desc())\
        .all()

# DELETE CUSTOMER
def delete_customer(db: Session, customer_id, company_id):

    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.company_id == company_id,
        Customer.is_active == True
    ).first()

    if not customer:
        return None

    customer.is_active = False
    db.commit()

    return customer
    



def update_customer(db, customer_id, data, company_id):

    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.company_id == company_id,
        Customer.is_active == True
    ).first()

    if not customer:
        return {"error": "Customer not found"}

    customer.name = data.name
    customer.phone = data.phone
    customer.email = data.email
    customer.address = data.address
    customer.gst_number = data.gst_number

    db.commit()
    db.refresh(customer)

    return customer    