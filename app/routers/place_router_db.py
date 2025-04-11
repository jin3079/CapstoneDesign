from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.schemas import Place, ResponseMessage
from app.services.place_service_db import (
    get_all_places, get_places_by_category,
    add_place, update_place,
    delete_place, count_places_by_date,
    count_operating_places_by_year, get_category_list,
    get_place_by_id
)

router = APIRouter(prefix="/places", tags=["장소"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{place_id}", response_model=Place)
def api_get_place(place_id: int, db: Session = Depends(get_db)):
    place = get_place_by_id(db, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="장소를 찾을 수 없습니다.")
    return place

@router.get("/", response_model=List[Place])
def api_get_all_places(category: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    if category:
        return get_places_by_category(db, category, status)
    return get_all_places(db, status)

@router.get("/categories", response_model=List[str])
def api_get_categories(db: Session = Depends(get_db)):
    return get_category_list(db)

@router.get("/timeline")
def api_timeline_stats(category: str, scale: str = Query("year", enum=["year", "month"]), db: Session = Depends(get_db)):
    data = count_places_by_date(db, category, scale)
    if data is None:
        raise HTTPException(status_code=404, detail="카테고리 없음")
    return data

@router.get("/timeline/operating")
def api_operating_timeline(category: str, from_year: int, to_year: int, db: Session = Depends(get_db)):
    data = count_operating_places_by_year(db, category, from_year, to_year)
    if data is None:
        raise HTTPException(status_code=404, detail="카테고리 없음")
    return data

@router.post("/", response_model=ResponseMessage)
def api_add_place(place: Place, db: Session = Depends(get_db)):
    add_place(db, place)
    return {"message": f"'{place.category}'에 장소가 추가되었습니다."}

@router.put("/{place_id}", response_model=ResponseMessage)
def api_update_place(place_id: int, place: Place, db: Session = Depends(get_db)):
    if not update_place(db, place_id, place):
        raise HTTPException(status_code=404, detail="해당 id 없음")
    return {"message": f"id={place_id} 항목 수정됨"}

@router.delete("/{place_id}", response_model=ResponseMessage)
def api_delete_place(place_id: int, db: Session = Depends(get_db)):
    if not delete_place(db, place_id):
        raise HTTPException(status_code=404, detail="해당 id 없음")
    return {"message": f"id={place_id} 항목 삭제됨"}
