from typing import Dict

from pydantic import BaseModel


class JsonQuery(BaseModel):
    ds: Dict
    WS: Dict
    WD: Dict
    y: Dict
