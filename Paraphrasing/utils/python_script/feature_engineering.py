import config
import pandas as pd
import numpy as np
#from pandas_description import describe_data
from sklearn import preprocessing

#function to fillna by mean
def fillna_mean(data_series):
    data_series =  data_series.fillna(data_series.mean())
    return data_series
#function to fillna by median
def fillna_meadian(data_series):
    data_series =  data_series.fillna(data_series.median())
    return data_series
#function to fillna by mode
def fillna_mode(data_series):
    data_series =  data_series.fillna(data_series.mode())
    return data_series
#function to fillna by backwardfill
def fillna_bfill(data_series):
    data_series =  data_series.fillna(method='bfill')
    return data_series
#function to fillna by forwardfill
def fillna_ffill(data_series):
    data_series =  data_series.fillna(method='ffill')
    return data_series
def apply_label_encoding(data_series):
    label_encoder = preprocessing.LabelEncoder()
    data_series = label_encoder.fit_transform(data_series)
    return data_series
