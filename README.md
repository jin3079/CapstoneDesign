# 장소 API 서버

## 실행 방법
- 'bash: uvicorn app.main:app --reload'

## 예시 요청
- 'GET /places/병원'
- 'GET /places/대피소?status=운영 중'
- 'POST /places/병원' => JSON 바디로 장소 추가
- 'PUT /places/병원/1' => id=1 항목 수정
- 'DELETE /places/병원/1' => id=1 항목 삭제

## 디렉토리 구조:
- 'core/': 앱 설정 (CORS 등)
- 'database/': 파일 기반 데이터 로딩/저장
- 'models/': 요청/응답 스키마 정의
- 'routers/': API 경로 정의
- 'services/': CRUD 로직 처리

# 📦 장소 API 서버 (FastAPI)

- 이 프로젝트는 JSON 기반으로 장소(병원, 대피소 등)를 조회/추가/수정/삭제할 수 있는 FastAPI 백엔드입니다.

---

## ✅ 실행 환경

- Python 3.10 이상
- pip
- (권장) 가상환경 사용

---

## 📁 설치 및 실행 방법

### 1. 프로젝트 클론
```bash
git clone <프로젝트 주소>
cd project_root

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
### 5. Swagger 문서 확인
http://localhost:8000/docs


## 프로젝트 구조
project_root/
├── app/
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── models/
│   ├── database/
│   ├── core/
│   └── data/            # 병원.json, 대피소.json 등
├── requirements.txt
└── README.md

## 예시 API 요청
GET	    /places/병원	    | 병원 목록 조회
POST	/places/병원	    | 병원 추가
PUT	    /places/병원/1	| 병원 정보 수정
DELETE	/places/병원/1	| 병원 삭제

