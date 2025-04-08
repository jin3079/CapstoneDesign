import os
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", 'data')

def load_place_data(category:str):
    filepath = os.path.join(DATA_DIR, f"{category}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

def save_place_data(category: str, data: dict):
    filepath = os.path.join(DATA_DIR, f"{category}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)   # type: ignore

def list_categories():
    return [filename.replace(".json", "")
            for filename in os.listdir(DATA_DIR)
            if filename.endswith(".json")]