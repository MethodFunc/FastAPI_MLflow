from sqlalchemy.orm import Session

from postgres import schemas, database, models


def insert_item(db: Session, name: str, schema: schemas.Scada):
    table = models.create_models(name)
    # Create Table
    database.ScadaBase.metadata.create_all(bind=database.scada_engine)
    table_item = table(record_date=schema.recode_date, wind_speed=schema.wind_speed,
                       wind_direction=schema.wind_direction, active_power=schema.active_power)

    db.add(table_item)
    db.commit()
    db.refresh(table_item)

    return table_item


def get_data(db: Session, time_: str, generator_name: str, start_date: str, end_date: str):
    # sql = f"-- select ds, ap from jeju.{generator_name} where ds>='{start_date}' AND ds<'{end_date}'"
    sql = f"select date_trunc('{time_}', ds) as ds, avg(ap) as ap from jeju.{generator_name} where ds>='{start_date}' and ds<='{end_date}' group by 1"
    result = db.execute(sql)
    data = result.fetchall()

    return data


def get_data2(db: Session, generator_name: str, start_date: str, end_date: str):
    sql = f"select ds, ap from jeju.{generator_name} where ds>='{start_date}' AND ds<='{end_date}'"
    result = db.execute(sql)
    data = result.fetchall()

    return data


