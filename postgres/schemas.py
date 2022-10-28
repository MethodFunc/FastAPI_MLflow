from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Scada(BaseModel):
    recode_date: Optional[datetime] = None
    wind_speed: float
    wind_direction: float
    active_power: float

    class Config:
        orm_mode = True
