from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from app.database.models import Place, Category
from app.models.schemas import Place as PlaceSchema

def convert_to_schema_list(places):
    return [
        PlaceSchema(
            id=p.id,
            name=p.name,
            lat=p.lat,
            lng=p.lng,
            status=p.status,
            built_year=p.built_year,
            built_month=p.built_month,
            built_date=p.built_date,
            capacity=p.capacity,
            category=p.category.name if p.category else None
        )
        for p in places
    ]

def get_all_places(db: Session, status: Optional[str] = None) -> List[Place]:
    query = db.query(Place).join(Category)
    if status:
        query = query.filter(Place.status == status)
    places = query.all()
    return convert_to_schema_list(places)

def get_places_by_category(db: Session, category_name: str, status: Optional[str] = None) -> List[PlaceSchema]:
    query = db.query(Place).join(Category).filter(Category.name == category_name)
    if status:
        query = query.filter(Place.status == status)
    places = query.all()
    return convert_to_schema_list(places)

def get_place_by_id(db: Session, place_id: int) -> Optional[PlaceSchema]:
    place = db.query(Place).join(Category).filter(Place.id == place_id).first()
    if not place:
        return None
    return PlaceSchema(
        id=place.id,
        name=place.name,
        lat=place.lat,
        lng=place.lng,
        status=place.status,
        built_year=place.built_year,
        built_month=place.built_month,
        built_date=place.built_date,
        capacity=place.capacity,
        category=place.category.name if place.category else None
    )

def add_place(db: Session, place: Place):
    category = db.query(Category).filter_by(name=place.category).first()
    if not category:
        category = Category(name=place.category)
        db.add(category)
        db.commit()
        db.refresh(category)

    new_place = Place(
        name=place.name,
        lat=place.lat,
        lng=place.lng,
        status=place.status,
        built_year=place.built_year,
        built_month=place.built_month,
        built_date=place.built_date,
        capacity=place.capacity,
        category_id=category.id
    )
    db.add(new_place)
    db.commit()

def add_category(db: Session, category_name: str) -> bool:
    existing = db.query(Category).filter_by(name=category_name).first()
    if existing:
        return False
    category = Category(name=category_name)
    db.add(category)
    db.commit()
    return True

def update_place(db: Session, place_id: int, place):
    target = db.query(Place).filter_by(id=place_id).first()
    if not target:
        return False

    target.name = place.name
    target.lat = place.lat
    target.lng = place.lng
    target.status = place.status
    target.built_year = place.built_year
    target.built_month = place.built_month
    target.built_date = place.built_date
    target.capacity = place.capacity

    category = db.query(Category).filter_by(name=place.category).first()
    if not category:
        category = Category(name=place.category)
        db.add(category)
        db.commit()
        db.refresh(category)

    target.category_id = category.id
    db.commit()
    return True

def delete_place(db: Session, place_id: int):
    place = db.query(Place).filter_by(id=place_id).first()
    if not place:
        return False
    db.delete(place)
    db.commit()
    return True

def delete_category(db: Session, category_name: str) -> bool:
    category = db.query(Category).filter_by(name=category_name).first()
    if not category:
        return False

    places = db.query(Place).filter_by(category_id=category.id).all()
    if places:
        return False

    db.delete(category)
    db.commit()
    return True

def count_places_by_date(db: Session, category_name: str, scale: str):
    category = db.query(Category).filter_by(name=category_name).first()
    if not category:
        return None

    if scale == "year":
        results = db.query(Place.built_year, func.count()).filter(Place.category_id == category.id).group_by(Place.built_year).order_by(Place.built_year).all()
        return {"scale": "year", "data": [{"year": r[0], "count": r[1]} for r in results]}

    elif scale == "month":
        results = db.query(Place.built_year, Place.built_month, func.count()).filter(Place.category_id == category.id).group_by(Place.built_year, Place.built_month).order_by(Place.built_year, Place.built_month).all()
        return {"scale": "month", "data": [{"year": r[0], "month": r[1], "count": r[2]} for r in results]}

    return None

def count_operating_places_by_year(db: Session, category_name: str, from_year: int, to_year: int):
    category = db.query(Category).filter_by(name=category_name).first()
    if not category:
        return None

    all_places = (
        db.query(Place.built_year)
        .filter(
            Place.category_id == category.id,
            Place.status == "운영 중",
            Place.built_year <= to_year  # 전체 누적 대상
        )
        .all()
    )

    year_counts = {}
    for year in range(from_year, to_year + 1):
        year_counts[year] = 0

    for place in all_places:
        for y in range(place.built_year, to_year + 1):
            if y in year_counts:
                year_counts[y] += 1

    return {"data": [{"year": y, "count": year_counts[y]} for y in sorted(year_counts.keys())]}

def get_category_list(db: Session):
    return [category.name for category in db.query(Category).all()]