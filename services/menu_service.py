from sqlalchemy.orm import selectinload
from models.menu import Menu

def get_menus(db):

    menus = (
        db.query(Menu)
        .options(selectinload(Menu.submenu))
        .filter(Menu.parent_id == None)
        .filter(Menu.is_active == True)
        .order_by(Menu.order_no)
        .all()
    )

    return menus