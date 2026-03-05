from sqlalchemy.orm import Session
from models.vendor import Vendor
from schemas.vendor_schema import VendorCreate, VendorUpdate
from sqlalchemy.orm import Session
from models.vendor import Vendor
from models.accounts import Account



def create_vendor(db: Session, data: VendorCreate, company_id: int):

    # 🔎 Check duplicate vendor code first
    existing = db.query(Vendor).filter(
        Vendor.company_id == company_id,
        Vendor.vendor_code == data.vendor_code
    ).first()

    if existing:
        raise ValueError("Vendor code already exists")

    # 🔎 Find Accounts Payable group
    payable_group = (
        db.query(Account)
        .filter(
            Account.company_id == company_id,
            Account.account_type == "LIABILITY",
            Account.name == "Accounts Payable",
            Account.is_group == False
        )
        .first()
    )

    if not payable_group:
        raise ValueError("Accounts Payable group not found")

    # 🧾 Create ledger for vendor
    vendor_ledger = Account(
        company_id=company_id,
        name=data.name,
        parent_id=payable_group.id,
        is_group=False,
        is_system=False,
        account_type="LIABILITY"
    )

    db.add(vendor_ledger)
    db.flush()   # get ledger ID

    # 👤 Create vendor
    vendor = Vendor(
        company_id=company_id,
        account_id=vendor_ledger.id,
        vendor_code=data.vendor_code,
        name=data.name,
        contact_person=data.contact_person,
        phone=data.phone,
        email=data.email,
        gst_number=data.gst_number,
        address=data.address,
        city=data.city,
        state=data.state,
        pincode=data.pincode
    )

    db.add(vendor)

    db.commit()
    db.refresh(vendor)

    return vendor


def list_vendors(db: Session, company_id: int):

    return db.query(Vendor)\
        .filter(Vendor.company_id == company_id)\
        .filter(Vendor.is_active == True)\
        .order_by(Vendor.name)\
        .all()


def update_vendor(db: Session, vendor_id: int, data: VendorUpdate):

    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()

    if not vendor:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(vendor, key, value)

    db.commit()
    db.refresh(vendor)

    return vendor


def delete_vendor(db: Session, vendor_id: int):

    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()

    if not vendor:
        return None

    vendor.is_active = False
    db.commit()

    return vendor