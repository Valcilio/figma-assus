import os
from random import choice
import pandas as pd
from pandas.testing import assert_frame_equal
import pickle
import pytest
import sys
sys.path.insert(0, os.environ.get('SRC_FIGMA_PATH'))

import resources.context as c
from timeseriesmodeling import TimeSeriesModeling

df_test_nopred = pickle.load(open(c.DATA_PROC_FLD / 'test_csv_no_pred.pkl', 'rb'))
df_test_pred = pickle.load(open(c.DATA_PROC_FLD / 'test_csv_with_pred.pkl', 'rb'))
test_rcross_val = pickle.load(open(c.DATA_INT_FLD / 'test_roll_cross_val.pkl', 'rb')) 

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

def test_rolling_cross_validation():
    '''Test rolling cross validation to see if it's outputing the correct value of performance'''

    scaler = 'log1p'
    roll_cross_val = ts_model.rolling_cross_validation(validations = 5, model=model, scaler=scaler, orig_name='close')

    return assert_frame_equal(test_rcross_val, roll_cross_val)