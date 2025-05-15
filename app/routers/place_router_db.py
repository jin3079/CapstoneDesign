from fastapi import APIRouter, HTTPException, Query, Depends, Response
from typing import Optional, List
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.schemas import Place, ResponseMessage, Category
from app.services.place_service_db import (
    get_all_places, get_places_by_category,
    add_place, update_place,
    delete_place, count_places_by_date,
    count_operating_places_by_year, get_category_list,
    get_place_by_id,
    add_category,
    delete_category,
)
import csv
import io

router = APIRouter(prefix="/places", tags=["장소"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/download-csv")
def download_places_csv(db: Session = Depends(get_db)):
    places = get_all_places(db)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "category", "lat", "lng", "status", "built_year", "built_month", "built_date", "capacity"])  # 컬럼 헤더

    for place in places:
        writer.writerow([
            place.id,
            place.name,
            place.category,
            place.lat,
            place.lng,
            place.status,
            place.built_year,
            place.built_month,
            place.built_date,
            place.capacity,
        ])

    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=places.csv"
    return response


@router.get("/categories", response_model=List[str])
def api_get_categories(db: Session = Depends(get_db)):
    return get_category_list(db)

@router.get("/", response_model=List[Place])
def api_get_all_places(category: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    if category:
        return get_places_by_category(db, category, status)
    return get_all_places(db, status)

@router.get("/timeline/operating")
def api_operating_timeline(category: str, from_year: int, to_year: int, db: Session = Depends(get_db)):
    data = count_operating_places_by_year(db, category, from_year, to_year)
    if data is None:
        raise HTTPException(status_code=404, detail="카테고리 없음")
    return data

@router.get("/timeline")
def api_timeline_stats(category: str, scale: str = Query("year", enum=["year", "month"]), db: Session = Depends(get_db)):
    data = count_places_by_date(db, category, scale)
    if data is None:
        raise HTTPException(status_code=404, detail="카테고리 없음")
    return data

@router.get("/{place_id}", response_model=Place)
def api_get_place(place_id: int, db: Session = Depends(get_db)):
    place = get_place_by_id(db, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="장소를 찾을 수 없습니다.")
    return place

@router.post("/", response_model=ResponseMessage)
def api_add_place(place: Place, db: Session = Depends(get_db)):
    add_place(db, place)
    return {"message": f"'{place.category}'에 장소가 추가되었습니다."}

@router.post("/categories", response_model=ResponseMessage)
def api_create_category(category: Category, db: Session = Depends(get_db)):
    success = add_category(db, category.name)
    if not success:
        raise HTTPException(status_code=400, detail="카테고리가 이미 존재합니다.")
    return {"message": f"'{category.name}' 카테고리가 추가되었습니다."}

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

@router.delete("/categories/{category_name}", response_model=ResponseMessage)
def api_delete_category(category_name: str, db: Session = Depends(get_db)):
    success = delete_category(db, category_name)
    if not success:
        raise HTTPException(status_code=400, detail="카테고리가 존재하지 않거나 연관된 장소가 있어 삭제할 수 없습니다.")
    return {"message": f"카테고리'{category_name}'가 삭제되었습니다."}
