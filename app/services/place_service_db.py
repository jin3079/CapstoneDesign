from sqlalchemy.orm import Session
from app.database.models import Place, Category

def get_all_places(db: Session):
    return db.query(Place).all()

def get_places_by_category(db: Session, category_name: str):
    return (
        db.query(Place)
        .join(Category)
        .filter(Category.name == category_name)
        .all()
    )