from pydantic import BaseModel
from datetime import date

class Place(BaseModel):
    id:int
    name:str
    lat:float
    lng:float
    status:str
    builtYear: int | None = None
    builtMonth: int | None = None
    builtDate: date | None = None
    capacity: int | None = None
    category: str | None = None

class ResponseMessage(BaseModel):
    message:str