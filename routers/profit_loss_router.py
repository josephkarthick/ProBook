from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from services.profit_loss_service import get_profit_loss

router = APIRouter(prefix="/profit-loss", tags=["Profit & Loss"])


@router.get("/")
def profit_loss(request: Request, db: Session = Depends(get_db)):

    company_id = request.session.get("company_id")

    return get_profit_loss(db, company_id)