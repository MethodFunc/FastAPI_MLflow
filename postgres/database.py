from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# todo: 2개로 만들기. 1 스카다 데이터 2 예측 데이터
SQLALCHEMY_DATABASE_URL1 = "postgresql+psycopg2://dev:dev1234@localhost:5432/data"
SQLALCHEMY_DATABASE_URL2 = "postgresql+psycopg2://dev:dev1234@localhost:5432/test"

data_engine = create_engine(
    SQLALCHEMY_DATABASE_URL1
)

scada_engine = create_engine(
    SQLALCHEMY_DATABASE_URL2
)

DataSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=data_engine)
ScadaSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=scada_engine)

DataBase = declarative_base(bind=data_engine)
ScadaBase = declarative_base(bind=scada_engine)
