import pandas as pd
import sqlalchemy.exc

from schemas.json_schema import JsonQuery
from .rmodules import prediction, rename_gen, scada_insert
from mlflows.loadmodel import load_model
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.encoders import jsonable_encoder
from postgres.database import ScadaSessionLocal

from sqlalchemy.orm import Session


def get_scada():
    db = ScadaSessionLocal()
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
async def json_query(generator: str, query: JsonQuery, db: Session = Depends(get_scada)):
    generator = rename_gen(generator)
    print(generator)

    data = jsonable_encoder(query)
    dataframe = pd.DataFrame(data)
    try:
        scada_insert(dataframe, generator, db)
    except sqlalchemy.exc.IntegrityError:
        print(f'Data is Exsits')

    model = load_model(generator)
    predict = prediction(model, dataframe)

    return predict
