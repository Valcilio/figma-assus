import os
from random import choice
import pandas as pd
from pandas.testing import assert_frame_equal
import pickle
import sys
sys.path.insert(0, os.environ.get('SRC_FIGMA_PATH'))

import resources.context as c
from resources.timeseriesmodeling import TimeSeriesModeling

df_test_nopred = pickle.load(open(c.DATA_PROC_FLD / 'test_csv_no_pred.pkl', 'rb'))
df_test_pred = pickle.load(open(c.DATA_PROC_FLD / 'test_csv_with_pred.pkl', 'rb'))

ts_model = TimeSeriesModeling(df=df_test_nopred)
model = ts_model.fit_sarimax()

def test_forecast_sarimax():
    '''Test default model (last) forecasting from the method forecast'''
    
    df_pred = ts_model.forecast()

    return assert_frame_equal(df_test_pred, df_pred)

def test_forecast_sarimax_with_model_passed():
    '''Test forecast with passing a fitted model'''

    df_pred = ts_model.forecast(fitted_model=model)

    return assert_frame_equal(df_test_pred, df_pred)