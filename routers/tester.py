import pandas as pd
import plotly.express as px
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from mlflows.loadmodel import load_model
from postgres.database import ScadaSessionLocal
from schemas.json_schema import JsonQuery
from .rmodules import scada_insert, rename_gen, prediction

router = APIRouter(
    prefix='/test',
    tags=['test'],
)


def get_scada():
    db = ScadaSessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/json_query/')
async def json_tester(generator: str, query: JsonQuery):
    generator = rename_gen(generator)
    data = jsonable_encoder(query)
    dataframe = pd.DataFrame(data)
    model = load_model(generator)
    predict = prediction(model, dataframe)
    print(predict)

    return predict


@router.get('/plot_test')
async def plot_test(data):
    fig = px.line(data, x='ds', y='ap', title='Tester')
    return fig.to_json()


@router.post('/json_query_insert_db_test')
async def json_query_insert_db(generator: str, query: JsonQuery, db: Session = Depends(get_scada)):
    generator = rename_gen(generator)

    data = jsonable_encoder(query)
    dataframe = pd.DataFrame(data)

    scada_insert(dataframe, generator, db)
