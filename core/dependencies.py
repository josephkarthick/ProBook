from fastapi import Request, HTTPException, Depends
from core.company_utils import get_current_company_id

def get_current_company(request: Request):

    company_id = request.session.get("company_id")

    if not company_id:
        raise HTTPException(
            status_code=400,
            detail="No active company selected"
        )

    return company_id