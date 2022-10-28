from sqlalchemy import Column,  Integer,  Float, DateTime

from .database import Base, ScadaBase


def create_models(tablename):
    class Scada(ScadaBase):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        record_date = Column(DateTime, unique=True)
        wind_speed = Column(Float)
        wind_direction = Column(Float)
        active_power = Column(Float)

        def __init__(self, record_date, wind_speed, wind_direction, active_power):
            self.record_date = record_date
            self.wind_speed = wind_speed
            self.wind_direction = wind_direction
            self.active_power = active_power

    return Scada
