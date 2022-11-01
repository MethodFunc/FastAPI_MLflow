from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Scada(BaseModel):
    recode_date: Optional[datetime] = None
    wind_speed: float
    wind_direction: float
    active_power: float

    class Config:
        orm_mode = True


class Forecast(BaseModel):
    recode_date: Optional[datetime] = None
    forecast: float

    class Config:
        orm_mode = True
