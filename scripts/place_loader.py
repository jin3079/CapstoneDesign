import os
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", 'data')

# 특정 카테고리의 장소 데이터를 로드하는 함수
def load_place_data(category:str):
    filepath = os.path.join(DATA_DIR, f"{category}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

# 특정 카테고리의 장소 데이터를 저장하는 함수
def save_place_data(category: str, data: dict):
    filepath = os.path.join(DATA_DIR, f"{category}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)   # type: ignore

# data 폴더 내의 모든 JSON 파일을 리스트로 반환
def list_categories():
    return [filename.replace(".json", "")
            for filename in os.listdir(DATA_DIR)
            if filename.endswith(".json")]