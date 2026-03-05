from fastapi.templating import Jinja2Templates
from database import SessionLocal
from models.company import Company
from services.menu_service import get_menus

templates = Jinja2Templates(directory="templates")


def render_template(template_name: str, request, context: dict = None):

    if context is None:
        context = {}

    db = SessionLocal()

    try:
        company_id = request.session.get("company_id")

        active_company = None

        if company_id:
            active_company = (
                db.query(Company)
                .filter(Company.id == company_id)
                .first()
            )

        menus = get_menus(db)

        # default context
        base_context = {
            "request": request,
            "active_company": active_company,
            "active_company_id": company_id,
            "menus": menus
        }

        # merge custom context
        base_context.update(context)

        return templates.TemplateResponse(template_name, base_context)

    finally:
        db.close()