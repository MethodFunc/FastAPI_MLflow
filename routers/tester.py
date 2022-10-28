import pandas as pd

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from schemas.json_schema import JsonQuery
from .rmodules import scada_insert, rename_gen
import plotly.express as px
from postgres.database import ScadaSessionLocal
from sqlalchemy.orm import Session

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


@router.post('/json_query/', response_model=JsonQuery)
async def json_tester(generator: str, query: JsonQuery):
    data = jsonable_encoder(query)
    print(pd.DataFrame(data))
    return data


@router.get('/plot_test')
async def plot_test(data):
    fig = px.line(data, x='ds', y='ap', title='Tester')
    return fig.to_json()


@router.post('/json_query_insert_db_test')
async def json_query_insert_db(generator: str, query: JsonQuery, db: Session=Depends(get_scada)):
    generator = rename_gen(generator)

    data = jsonable_encoder(query)
    dataframe = pd.DataFrame(data)

    scada_insert(dataframe, generator, db)
