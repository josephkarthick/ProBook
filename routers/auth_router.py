from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from core.template_engine import templates


router = APIRouter()


# Login page
@router.get("/login")
def login_page(request: Request):

    return templates.TemplateResponse(
        "ProBook/Auth/login.html",
        {"request": request}
    )


# Login submit
@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username,
        User.password == password
    ).first()

    if not user:
        return templates.TemplateResponse(
            "ProBook/Auth/login.html",
            {
                "request": request,
                "error": "Invalid username or password"
            }
        )

    request.session["user_id"] = user.id
    request.session["role"] = user.role

    return RedirectResponse("/", status_code=302)


# Logout


@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse("/login", status_code=302)