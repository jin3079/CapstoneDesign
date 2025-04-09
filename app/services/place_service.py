from datetime import datetime

from app.database.place_loader import load_place_data, save_place_data
from app.models.schemas import Place
from collections import Counter

def fill_built_date(item: dict): # builtDate가 없으면 builtYear와 builtMonth로 생성하여 추가하는 함수
    if not item.get("builtDate"):
        year = item.get("builtYear")
        month = item.get("builtMonth") or 1
        if year:
            item['builtDate'] = f"{year}-{month:02d}-01"
    return item

def get_places(category: str, status: str | None = None): # 특정 카테고리의 장소 리스트 반환 (옵션: status 필터링)
    data = load_place_data(category)
    if data is None:
        return None
    data = [fill_built_date(p) for p in data]
    if status:
        data = [p for p in data if p.get("status") == status]
    return data

def count_places_by_date(category: str, scale: str): # 카테고리 내 장소들을 연도 또는 연-월 단위로 개수 집계
    data = load_place_data(category)
    if data is None:
        return None
    data = [fill_built_date(p) for p in data]
    counts = Counter()
    for item in data:
        date_str = item.get("builtDate")
        if date_str:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                key = f"{dt.year}" if scale == "year" else f"{dt.year}-{dt.month:02d}"
                counts[key] += 1
            except ValueError:
                continue
    return dict(sorted(counts.items()))

def count_operating_places_by_year(category: str, from_year: int, to_year: int): # 특정 연도 범위 내에 "운영 중"인 장소들의 수를 연도별로 집계
    data = load_place_data(category)
    if data is None:
        return None
    data = [fill_built_date(p) for p in data]
    counter = {}
    for year in range(from_year, to_year + 1):
        count = 0
        for item in data:
            built = item.get("builtYear")
            status = item.get("status")
            if built and built <= year and status == "운영 중":
                count += 1
        counter[str(year)] = count
    return counter

def add_place(category: str, place: Place): # 새로운 장소 데이터 추가
    data = load_place_data(category) or []
    item = place.model_dump()
    item = fill_built_date(item)
    data.append(item)
    save_place_data(category, data)

def update_place(category: str, place_id: int, place: Place): # 기존 장소 수정
    data = load_place_data(category)
    if data is None:
        return False
    for i, item in enumerate(data):
        if item.get("id") == place_id:
            updated = place.model_dump()
            updated = fill_built_date(updated)
            data[i] = updated
            save_place_data(category, data)
            return True
    return False

def delete_place(category: str, place_id: int): # 특정 id의 장소 삭제
    data = load_place_data(category)
    if data is None:
        return False
    new_data = [item for item in data if item.get("id") == place_id]
    if len(new_data) == len(data):
        return False
    save_place_data(category, new_data) #type: ignore
    return True