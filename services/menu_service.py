from models.menu import Menu


def get_menus(db, current_path: str):

    menus = db.query(Menu)\
        .filter(Menu.is_active == 1)\
        .order_by(Menu.order_no)\
        .all()

    parent_menus = []
    menu_map = {}

    # prepare menu objects
    for menu in menus:
        menu.submenu = []
        menu.active = False
        menu_map[menu.id] = menu

    # build tree
    for menu in menus:
        if menu.parent_id:
            parent = menu_map.get(menu.parent_id)
            if parent:
                parent.submenu.append(menu)
        else:
            parent_menus.append(menu)

    # mark active items
    for parent in parent_menus:
        for child in parent.submenu:
            if current_path.startswith(child.url):
                child.active = True
                parent.active = True

    return parent_menus