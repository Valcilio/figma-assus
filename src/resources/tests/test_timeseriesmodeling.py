import os
from random import choice
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
import sys
sys.path.insert(0, os.environ.get('SRC_FIGMA_PATH'))

import resources.context as c
from resources.datatransform import DataTransform
#from resources.timeseriesmodeling import TimeSeriesModeling

#df_test = pd.read_csv(c.DATA_INT_FLD / 'test_predict.py')
#ts_model = TimeSeriesModeling(df=df_test)

@pytest.fixture
def test_predict_arima_model():

    predict, model = ts_model.predict_arima_model()

    return assert_frame_equal(df_test, predict)

@pytest.fixture
def test_predict_sarimax_model():

    predict, model = ts_model.predict_sarimax_model()

    return assert_frame_equal(df_test, predict)