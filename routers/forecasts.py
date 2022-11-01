import pandas as pd
import sqlalchemy.exc
from fastapi import APIRouter, File
from fastapi.encoders import jsonable_encoder

from mlflows.loadmodel import load_model
from postgres.database import ScadaSessionLocal, DataSessionLocal
from schemas.json_schema import JsonQuery
from .rmodules import prediction, rename_gen, scada_insert, forecast_insert, scada_update, forecast_update

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
async def json_query(generator: str, query: JsonQuery):
    generator = rename_gen(generator)

    data = jsonable_encoder(query)
    dataframe = pd.DataFrame(data)
    print('asdf')
    try:
        with ScadaSessionLocal() as db:
            scada_insert(dataframe, generator, db)
    except sqlalchemy.exc.IntegrityError:
        with ScadaSessionLocal() as db:
            scada_update(dataframe, generator, db)

    model = load_model(generator)
    predict = prediction(model, dataframe)

    try:
        with DataSessionLocal() as db2:
            forecast_insert(predict, generator, db2)
    except sqlalchemy.exc.IntegrityError:
        with DataSessionLocal() as db2:
            forecast_update(predict, generator, db2)

    return predict
