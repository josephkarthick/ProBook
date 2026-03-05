from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from schemas.vendor_schema import VendorCreate
from services.vendor_service import create_vendor
from core.company_utils import get_current_company_id
from database import get_db
from schemas.vendor_schema import VendorCreate, VendorUpdate

from services.vendor_service import (
    create_vendor,
    list_vendors,
    update_vendor,
    delete_vendor
)

router = APIRouter(prefix="/vendors", tags=["Vendors"])



@router.post("/")
def create_vendor_api(
    data: VendorCreate,
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    try:
        return create_vendor(db, data, company_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def list_vendors_api(
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = request.session.get("company_id")

    return list_vendors(db, company_id)


@router.put("/{vendor_id}")
def update_vendor_api(
    vendor_id: int,
    data: VendorUpdate,
    db: Session = Depends(get_db)
):

    vendor = update_vendor(db, vendor_id, data)

    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    return vendor


@router.delete("/{vendor_id}")
def delete_vendor_api(
    vendor_id: int,
    db: Session = Depends(get_db)
):

    vendor = delete_vendor(db, vendor_id)

    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    return {"message": "Vendor deleted"}