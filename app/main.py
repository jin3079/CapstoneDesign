from fastapi import FastAPI
from app.core.config import setup_cors
from app.routers.place_router import router as place_router

app = FastAPI()
setup_cors(app)
app.include_router(place_router)

@app.get("/")
def root():
    return {"message": "Place API Server."}
