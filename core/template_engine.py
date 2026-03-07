from fastapi.templating import Jinja2Templates
from database import SessionLocal
from models.company import Company
from services.menu_service import get_menus

templates = Jinja2Templates(directory="templates")


def render_template(template_name, request, context=None):

    if context is None:
        context = {}

    db = SessionLocal()

    try:

        company_id = request.session.get("company_id")

        active_company = None

        if company_id:
            active_company = db.query(Company)\
                .filter(Company.id == company_id)\
                .first()

        menus = get_menus(db, request.url.path)

        base_context = {
            "request": request,
            "menus": menus,
            "active_company": active_company
        }

        base_context.update(context)

        return templates.TemplateResponse(template_name, base_context)

    finally:
        db.close()


# 🚫 Prevent misuse
def template_response(*args, **kwargs):
    raise Exception(
        "Use render_template() instead of templates.TemplateResponse()"
    )

templates.TemplateResponse = template_response