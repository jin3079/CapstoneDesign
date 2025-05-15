from pydantic import BaseModel
from datetime import date

class Place(BaseModel):
    id:int
    name:str
    lat:float
    lng:float
    status:str
    built_year: int | None = None
    built_month: int | None = None
    built_date: date | None = None
    capacity: int | None = None
    category: str | None = None

class Category(BaseModel):
    name:str

class ResponseMessage(BaseModel):
    message:str