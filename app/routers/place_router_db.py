from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.services.place_service_db import get_all_places, get_places_by_category

router = APIRouter(prefix="/places/db", tags=["DB 장소"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def api_get_all_places(db: Session = Depends(get_db)):
    return get_all_places(db)

@router.get("/filter")
def api_get_by_category(category: str, db: Session = Depends(get_db)):
    return get_places_by_category(db, category)
