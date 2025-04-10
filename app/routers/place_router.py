from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models.schemas import Place, ResponseMessage
from app.services.place_service import (
    get_places, get_all_places, add_place, update_place, delete_place,
    count_places_by_date, count_operating_places_by_year
)
from app.database.place_loader import list_categories


router = APIRouter(prefix="/places", tags=["장소"])

@router.get("/all", response_model=List[Place])
def api_get_all_places(status: Optional[str] = None):
    places = get_all_places(status)
    return places

@router.get("/categories", response_model=List[str]) # [GET] /places/categories - 존재하는 모든 카테고리 목록 반환
def api_get_categories():
    return list_categories()

@router.get("/{category}", response_model=List[Place]) # [GET] /places/{category} - 특정 카테고리의 장소 목록 조회 (필요시 status 필터 적용)
def api_get_places(category: str, status: Optional[str] = None):
    places = get_places(category, status)
    if places is None:
        raise HTTPException(status_code=404, detail="카테고리 없음")
    return places

@router.get("/{category}/timeline") # [GET] /places/{category}/timeline - 카테고리 내 장소 등록 수를 연도/월 단위로 집계하여 반환
def api_timeline_stats(category: str, scale: str = Query("year", enum=["year", "month"])):
    data = count_places_by_date(category, scale)
    if data is None:
        raise HTTPException(status_code=404, detail="카테고리 없음")
    return data

@router.get("/{category}/timeline/operating") # [GET] /places/{category}/timeline/operating - 특정 기간 내 운영 중인 장소 수를 연도별로 반환
def api_operating_timeline(category: str, from_year: int, to_year: int):
    data = count_operating_places_by_year(category, from_year, to_year)
    if data is None:
        raise HTTPException(status_code=404, detail="카테고리 없음")
    return data

@router.post("/{category}", response_model=ResponseMessage) # [POST] /places/{category} - 새 장소 추가
def api_add_place(category: str, place: Place):
    add_place(category, place)
    return {"message":f"'{category}' 에 장소가 추가되었습니다."}

@router.put("/{category}/{place_id}", response_model=ResponseMessage) # [PUT] /places/{category}/{place_id} - 기존 장소 정보 수정
def api_update_place(category: str, place_id: int, place: Place):
    if not update_place(category, place_id, place):
        raise HTTPException(status_code=404, detail="해당 id 없음")
    return {"message":f"id={place_id} 항목 수정됨"}

@router.delete("/{category}/{place_id}", response_model=ResponseMessage) # [DELETE] /places/{category}/{place_id} - 장소 삭제
def api_delete_place(category: str, place_id: int):
    deleted = delete_place(category, place_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="해당 id 없음")
    return {"message": f"id={place_id} 항목 삭제됨"}