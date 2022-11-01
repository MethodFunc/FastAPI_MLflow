# **FastAPI** with **MLflow** Server
**샘플데이터는 제공하지 않습니다.**<br>
**기본 파이썬 가상환경은 아나콘다 혹은 미니콘다로 구성하는것을 추천(pip로 오류걸리는 라이브러리들이 간혹 있음)**
## 0. 변경점
1. ~ 2022.10.30 - FastAPI 구축 데이터베이스 연동 기초 작업, Mlflow 다운로더 추가, 웹페이지 구성작업 
2. 2022.10.31 - 데이터베이스 Insert 연동, 그래프 일시 삭제
3. 2022.11.01 - 데이터베이스 업데이트 추가, 전처리 과정에 데이터레인지 추가

## 1. 시스템 요구사항
###  python: 3.7 or upper
- pandas: 1.4.3
- numpy: 1.19.5
- neuralprophet: 0.3.2
- SQLAlchemy 1.4.42
- mlflow 1.30.0
- pysftp
- psycopg2 -> conda 설치 추천
- plotly
- fastapi

### Database
- postgresql

### Bin 폴더
- MLflow로 동작 수행 시 해당 부분의 코드가 들어 있는 파일이 없으면 작동하지 않아서 넣음

## 2. 작동 샘플 이미지
### 메인 페이지 
api서버 접속 불가 시 당근이 붉게 변합니다.
![](readme_img/main_page.png)

### SwaggerUI
![](readme_img/swagger_ui.png)

### API Sample
![](readme_img/redoc.png)


### URL
Main: http://127.0.0.1:8000

Docs: http://127.0.0.1:8000/docs

redoc: http://127.0.0.1:8000/redoc

