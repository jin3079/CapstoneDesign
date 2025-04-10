from fastapi import FastAPI
from app.core.config import setup_cors
from app.routers.place_router import router as place_router
from app.routers.place_router_db import router as db_place_router
from app.database import models
from app.database.db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
setup_cors(app)
app.include_router(place_router)
app.include_router(db_place_router)

@app.get("/")
def root():
    return {"message": "Place API Server."}
