from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.grn_service import create_grn

router = APIRouter(prefix="/api/grn", tags=["GRN"])


@router.post("/")
def create_goods_receipt(data: dict, db: Session = Depends(get_db)):
    return create_grn(db, data)