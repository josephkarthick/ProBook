from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from database import get_db
from core.template_engine import render_template
from models.customer import Customer

router = APIRouter(prefix="/customers", tags=["Customer UI"])


@router.get("/{customer_id}/ledger")
def customer_ledger_page(
    request: Request,
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    return render_template(
        "ProBook/Contacts/customer_ledger.html",
        request,
        {
            "customer": customer
        }
    )