import os
import json
from datetime import date
from app.database.db import SessionLocal
from app.database.models import Category, Place

DATA_DIR = os.path.join(os.path.dirname(__file__), "app", "data")

def fill_built_date(item):
    year = item.get("builtYear")
    month = item.get("builtMonth") or 1
    if year:
        return date(year, month, 1)
    return None

db = SessionLocal()

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".json"):
        category_name = filename.replace(".json", "")
        filepath = os.path.join(DATA_DIR, filename)

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        # 카테고리가 없으면 생성
        category = db.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.commit()
            db.refresh(category)

        for item in data:
            existing = db.query(Place).filter_by(name=item["name"], category_id=category.id).first()
            if existing:
                continue

            place = Place(
                name=item["name"],
                lat=item["lat"],
                lng=item["lng"],
                status=item.get("status"),
                built_year=item.get("builtYear"),
                built_month=item.get("builtMonth"),
                built_date=fill_built_date(item),
                capacity=item.get("capacity"),
                category_id=category.id
            )
            db.add(place)

        db.commit()
        print(f"✅ {category_name} 데이터 삽입 완료")