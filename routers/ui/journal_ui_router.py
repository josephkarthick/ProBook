from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter()

@router.get("/journals")
def journals_page(request: Request):

    return render_template(
        "ProBook/Accounts/journals.html",
        request
    )