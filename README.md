# 📦 장소 API 서버 (FastAPI)

- 지역 기반 시설 데이터를 수집·저장하고, 연도별·월별로 통계 및 시각화할 수 있는 FastAPI 기반의 백엔드 프로젝트입니다.
- 병원, 대피소 등 다양한 장소 데이터를 CRUD 처리가능

---

## ✅ 실행 환경

- Python 3.10 이상
- pip
- (권장) 가상환경 사용

---

## 🛠️ 사용 기술

- **FastAPI** – Python 기반 비동기 웹 프레임워크  
- **Pydantic** – 데이터 유효성 검증 및 직렬화  
- **Uvicorn** – ASGI 서버  
- **JSON** – 파일 기반 데이터 저장  
- **(Optional)** MySQL, Firebase, PostgreSQL 등으로 확장 가능  

---

## 📊 주요 기능

- 카테고리 기반 장소 CRUD
- builtDate 기준 연/월별 생성 통계
- 운영 중 장소 연도별 누적 분석
- CORS 허용 → 프론트와 연동 가능
- Firebase / MySQL / PostgreSQL 등 DB 확장 가능

---

## 📁 설치 및 실행 방법
```bash
### 1. 프로젝트 클론

git clone <프로젝트 주소>
cd project

### 2. 가상환경 생성 및 활성화
# Windows
python -m venv venv
venv\\Scripts\\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

### 3. 필요한 패키지 설치
pip install -r requirements.txt

### 4. 서버 실행
uvicorn app.main:app --reload
```
### Swagger 문서 확인
http://localhost:8000/docs

---

## 프로젝트 구조
project_root/  
├── app/  
│   ├── main.py  
│   ├── routers/  
│   ├── services/  
│   ├── models/  
│   ├── database/  
│   ├── core/  
│   └── data/  
├── requirements.txt  
└── README.md  

---

## 🔌 API 예시
GET     /places/병원	                                            "병원 전체 목록 조회"  
GET     /places/병원?status=운영 중	                            "운영 중인 병원만 필터링"  
POST	/places/병원	                                            "새 병원 데이터 추가"  
PUT     /places/병원/1	                                        "ID=1 병원 수정"  
DELETE	/places/병원/1	                                        "ID=1 병원 삭제"  
GET	    /places/병원/timeline?scale=year	                        "연도별 생성 통계"  
GET	    /places/병원/timeline/operating?from_year&to_year	    "누적 운영 중 병원 수"  
GET	    /places/categories	                                    "등록된 카테고리 목록"  

---

작성자: 소프트웨어학부_20203079_서하진