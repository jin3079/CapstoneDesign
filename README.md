# 📦 장소 API 서버 (FastAPI + PostgreSQL)

지역 기반 시설 데이터를 수집·저장하고, 연도별·월별로 통계 및 시각화할 수 있는 FastAPI 기반 백엔드 프로젝트입니다. 
병원, 대피소 등 다양한 장소 데이터를 CRUD 및 통계 조회 가능하며, PostgreSQL을 기본 DB로 사용합니다.

---

## ✅ 실행 환경

- Python 3.10 이상
- pip
- (권장) 가상환경 사용
- PostgreSQL 13 이상

---

## 🛠️ 사용 기술

- **FastAPI** – Python 기반 비동기 웹 프레임워크  
- **Pydantic** – 데이터 유효성 검증 및 직렬화  
- **SQLAlchemy** – ORM 기반 DB 연동  
- **PostgreSQL** – 관계형 데이터베이스  
- **Uvicorn** – ASGI 서버

---

## 📊 주요 기능

- 카테고리 기반 장소 CRUD
- 단일 장소 상세 조회 (id 기반)
- builtDate 기준 연/월별 생성 통계
- 운영 중 장소 연도별 누적 분석
- 카테고리 목록 조회
- Swagger 문서 자동화
- CORS 허용 → 프론트엔드와 연동 가능
- CSV 파일 다운로드 기능

---

## 📁 설치 및 실행 방법
```bash
### 1. 프로젝트 클론
git clone <프로젝트 주소>
cd project

### 2. 가상환경 생성 및 활성화
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

### 3. 패키지 설치
pip install -r requirements.txt

### 4. PostgreSQL 설정 후 서버 실행
uvicorn app.main:app --reload
```

### Swagger 문서 확인
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📄 프로젝트 구조
```
project/
├── app/
│   ├── main.py                # FastAPI 앱 시작점
│   ├── routers/               # API 라우터 모음
│   ├── services/              # DB 접근 로직 모음
│   ├── models/                # Pydantic 응답 모델
│   ├── database/              # SQLAlchemy 설정 및 모델
│   └── core/                  # CORS 등 설정 모듈
├── requirements.txt
└── README.md
```

---

## 📍 API 목록

| Method | Endpoint                                                              | 설명                               |
|--------|-----------------------------------------------------------------------|----------------------------------|
| GET    | `/places`                                                             | 전체 장소 조회 (category/status 필터 가능) |
| GET    | `/places/{place_id}`                                                  | 특정 장소 상세 조회                      |
| POST   | `/places`                                                             | 새 장소 추가                          |
| PUT    | `/places/{place_id}`                                                  | 장소 수정                            |
| DELETE | `/places/{place_id}`                                                  | 장소 삭제                            |
| GET    | `/places/categories`                                                  | 등록된 카테고리 목록 조회                   |
| POST   | `/places/categories`                                                  | 새 카테고리 추가                        |
| DELETE | `/places/categories/{category_name}`                                  | 카테고리 삭제                          |
| GET    | `/places/timeline?category=병원&scale=year`                             | 연도별 생성 장소 수 통계                   |
| GET    | `/places/timeline/operating?category=병원&from_year=2020&to_year=2024`  | 운영 중인 장소 누적 수 통계                 |   
| GET    | `/places/download-csv`                                                | csv파일 다운로드                       |

---

작성자: 국민대학교 소프트웨어학부 20203079 서하진