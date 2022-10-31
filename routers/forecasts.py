import pandas as pd
import sqlalchemy.exc

from schemas.json_schema import JsonQuery
from .rmodules import prediction, rename_gen, scada_insert, forecast_insert
from mlflows.loadmodel import load_model
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.encoders import jsonable_encoder
from postgres.database import ScadaSessionLocal, scada_engine, DataSessionLocal, data_engine

from sqlalchemy.orm import Session


def get_scada():  # Scada Data
    db = ScadaSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_forecast():  # Forecast
    db = DataSessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix='/forecast',
    tags=['forecast']
)


@router.post('/files')
async def predict_file(generator: str, file: UploadFile = File(...)):
    generator = rename_gen(generator)

    if file.content_type == "text/csv":
        dataframe = pd.read_csv(file.file)
    elif file.content_type == "application/json":
        dataframe = pd.read_json(file.file)

    model = load_model(generator)

    predict = prediction(model, dataframe)

    return predict


@router.post('/json_query')
async def json_query(generator: str, query: JsonQuery, db: Session = Depends(get_scada),
                     db2: Session = Depends(get_forecast)):
    generator = rename_gen(generator)

    data = jsonable_encoder(query)
    dataframe = pd.DataFrame(data)
    print('asdf')
    try:
        scada_insert(dataframe, generator, db)
    except sqlalchemy.exc.IntegrityError:
        print(f'Data is Exsits')

    model = load_model(generator)
    predict = prediction(model, dataframe)

    try:
        forecast_insert(predict, generator, db2)

    except sqlalchemy.exc.IntegrityError:

        print(f'Data is Exsits')

    return predict
