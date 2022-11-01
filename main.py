import json

import pandas as pd
import plotly.express as px
import plotly.utils
import requests
import sqlalchemy.exc
import uvicorn
from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from postgres.crud import get_data, get_data2
from postgres.database import DataSessionLocal
from routers import tester, forecasts


def get_db():
    db = ...
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if (request.url.path.startswith("/v1") and
            request.headers.get('X-Token', None) != "expected_token"):
        return JSONResponse(status_code=403)
    response = await call_next(request)
    return response


app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")

app.include_router(tester.router)
app.include_router(forecasts.router)


def server_status(url):
    status = requests.get(url).status_code
    if status == 200:
        code = 'Active'
    else:
        code = 'Unable to connect to server'

    return code


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    # API Server URL
    api_url = '*'
    mlflow_url = 'http://localhost:5000/'
    api = server_status(api_url)
    mlflow = server_status(mlflow_url)

    return templates.TemplateResponse('index.html', {'request': request, 'status': api, 'mlflow': mlflow})


@app.post('/', response_class=HTMLResponse)
async def index_item(request: Request, time_: str = Form(...), gen: str = Form(...), start: str = Form(...),
                     end: str = Form(...),
                     db: Session = Depends(get_db)):
    # API Server URL
    api_url = '*'
    mlflow_url = 'http://localhost:5000/'
    api = server_status(api_url)
    mlflow = server_status(mlflow_url)
    gen_lower = gen.lower()

    try:
        if time_ == 'default':
            data = get_data2(db, gen_lower, start, end)
        else:
            data = get_data(db, time_, gen_lower, start, end)
    except sqlalchemy.exc.ProgrammingError:
        raise HTTPException(status_code=404, detail='Input data is fault')

    data = pd.DataFrame(data)
    if not data.empty:

        data = data.sort_values('ds')

        fig = px.line(data, x='ds', y='ap', title=f'{gen}:{start} ~ {end}')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graphJSON = 'Empty Database'

    return templates.TemplateResponse('index.html',
                                      {'request': request, 'result': graphJSON, 'status': api, 'mlflow': mlflow})


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, debug=True)
