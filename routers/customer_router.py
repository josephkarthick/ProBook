from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db

from schemas.customer_schema import CustomerCreate
from services.customer_service import (
    create_customer,
    list_customers,
    delete_customer,
    update_customer
)

router = APIRouter(prefix="/api/customers", tags=["Customers"])


# LIST
@router.get("/")
def get_customers(request: Request, db: Session = Depends(get_db)):
    company_id = request.session.get("company_id")
    return list_customers(db, company_id)


# CREATE
@router.post("/")
def create_customer_api(
    data: CustomerCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    company_id = request.session.get("company_id")
    return create_customer(db, data, company_id)


# UPDATE
@router.put("/{customer_id}")
def update_customer_api(
    customer_id: int,
    data: CustomerCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    company_id = request.session.get("company_id")
    return update_customer(db, customer_id, data, company_id)


# DELETE
@router.delete("/{customer_id}")
def delete_customer_api(
    customer_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    company_id = request.session.get("company_id")
    return delete_customer(db, customer_id, company_id)