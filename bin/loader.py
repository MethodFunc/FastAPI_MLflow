import numpy as np
import pandas as pd
from pyarrow import csv
from copy import deepcopy


def load_dataframe(path, col_name):
    dataframe = csv.read_csv(path).to_pandas()
    modify_data = dataframe.copy()
    modify_data.rename(columns={
        '': 'ds',
        'AP': 'y'
    }, inplace=True)
    modify_data['ds'] = pd.to_datetime(modify_data['ds'])
    modify_data.set_index('ds', inplace=True)
    modify_data = modify_data.resample('10s').mean()
    modify_data.fillna(method='ffill', inplace=True)
    modify_data.fillna(method='bfill', inplace=True)
    col_list = deepcopy(col_name)
    col_list.append('y')
    modify_data = modify_data[col_list]
    modify_data = modify_data.resample('1h').mean()
    modify_data.reset_index(inplace=True)

    return modify_data


def split_dataframe(dataframe):
    data_size = len(dataframe)
    train_size = int(data_size * 0.9)
    train_data = dataframe[:train_size]
    validation_data = dataframe[train_size:]

    return train_data, validation_data
