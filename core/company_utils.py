from fastapi import Request, HTTPException

def get_current_company_id(request: Request) -> int:

    company_id = request.session.get("company_id")

    if company_id is None:
        raise HTTPException(
            status_code=400,
            detail="No active company selected"
        )

    return int(company_id)