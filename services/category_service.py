from sqlalchemy.orm import Session
from models.item_category import ItemCategory


def list_categories(db: Session, company_id: int):

    return db.query(ItemCategory)\
        .filter(ItemCategory.company_id == company_id)\
        .order_by(ItemCategory.name)\
        .all()