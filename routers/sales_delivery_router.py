from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from services.delivery_service import create_delivery_note

router = APIRouter(prefix="/api/deliveries", tags=["Delivery"])


@router.post("/")
def create_delivery(data: dict, db: Session = Depends(get_db)):
    return create_delivery_note(db, data, company_id=1)


@router.get("/")
def list_deliveries():
    return {"message": "list deliveries"}


@router.get("/{delivery_id}")
def get_delivery(delivery_id: int):
    return {"message": f"delivery {delivery_id}"}