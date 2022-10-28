from datetime import datetime

import pandas as pd
from postgres.crud import insert_item
from postgres.schemas import Scada
from sqlalchemy.orm import Session


def prediction(model, dataframe) -> list:
    dataframe.dropna(inplace=True)
    dataframe['ds'] = pd.to_datetime(dataframe['ds'])

    # 사이 결측값 확인
    dataframe.set_index('ds', inplace=True)
    dataframe = dataframe.resample('1H').mean()

    # 결측 값이 있으면 결측값 채우기
    if dataframe.isna().sum().sum() != 0:
        dataframe.fillna(method='ffill', inplace=True)
        dataframe.fillna(method='bfill', inplace=True)

    # NerualProphet Forecast 데이터프레임 구조 만들기
    dataframe.reset_index(inplace=True)
    indices = pd.date_range(start=dataframe['ds'].values[-1], periods=25, freq='H')[1:]
    se = pd.DataFrame(indices, columns=['ds'])
    sample = pd.concat([dataframe, se], axis=0, ignore_index=True)

    # 예측
    predict = model.predict(sample)

    # 예측 값 정리
    cols = [col for col in predict.columns if 'yhat' in col]
    indices = predict['ds'][24:]
    predict = predict[cols].sum()

    output = {index: value for index, value in zip(indices, predict)}

    return output


# Scada Data Table Insert
def scada_insert(dataframe, gen_name, db: Session):
    print('insert start')
    for _, values in dataframe.iterrows():
        date = datetime.strptime(values['ds'], '%Y.%m.%d %H:%M')
        item = Scada(recode_date=date, wind_speed=values['WS'], wind_direction=values['WD'],
                     active_power=values['y'])

        insert_item(db, gen_name, schema=item)


def rename_gen(generator_name):
    rename_generator = {'DB01': 'DB_HJ01',
                        'DB02': 'DB_HJ02',
                        'DB03': 'DB_HJ03',
                        'DB04': 'DB_HJ04',
                        'DB05': 'DB_HJ05',
                        'DB06': 'DB_HJ06',
                        'DB07': 'DB_HJ07',
                        'DB08': 'DB_HJ08',
                        'DB09': 'DB_HJ09',
                        'DB10': 'DB_HJ10',
                        'DB11': 'DB_HJ11',
                        'DB12': 'DB_HJ12',
                        'DB13': 'DB_HJ13',
                        'DB14': 'DB_HJ14',
                        'DB15': 'DB_HJ15',
                        'GN02': 'GN_US01',
                        'GS07': 'GS_HJ01',
                        'GS08': 'GS_HJ02',
                        'GS09': 'GS_HJ03',
                        'GS10': 'GS_HJ04',
                        'GS11': 'GS_HJ05',
                        'GS12': 'GS_HJ06',
                        'GS13': 'GS_HJ07',
                        'GS01': 'GS_HS01',
                        'GS02': 'GS_US01',
                        'GS03': 'GS_HS03',
                        'GS04': 'GS_US02',
                        'GS05': 'GS_US03',
                        'HW17': 'HW_DS01',
                        'HW16': 'HW_HD01',
                        'HW05': 'HW_HJ01',
                        'HW04': 'HW_US01',
                        'HW06': 'HW_VT01',
                        'HW10': 'HW_VT04',
                        'HW11': 'HW_VT05',
                        'HW13': 'HW_VT07',
                        'HW14': 'HW_VT08',
                        'HW15': 'HW_VT09',
                        'SC01': 'SC_VT01',
                        'SC02': 'SC_VT02'}

    if generator_name.islower:
        generator = generator_name.upper()

    gen_ = rename_generator.get(generator)

    if gen_ is None:
        gen_ = generator

    return gen_