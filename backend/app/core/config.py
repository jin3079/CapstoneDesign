from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# CORS 설정을 앱에 적용하는 함수
def setup_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,     #type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
