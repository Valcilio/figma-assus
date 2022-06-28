import os
from random import choice
import pandas as pd
from pandas.testing import assert_frame_equal
import sys
sys.path.insert(0, os.environ.get('SRC_FIGMA_PATH'))

from datatransform import DataTransform
from resources import context as c

df_test = pd.read_csv(c.DATA_INT_FLD / 'test_df.csv')
data_trans = DataTransform(date_col='timestamp', df=df_test)

def test_check_dateindex():
    '''Test if is checking if the index is datetime index correctly'''

    dateindex_check = data_trans.check_dateindex()

    assert dateindex_check == 0

def test_transform_dateindex():
    '''Test if this method is transforming the index in datetime index'''

    df = data_trans.transform_dateindex(date_index_check = 0)
    df['test'] = 1
    df = df['test'].reset_index().select_dtypes('datetime64[ns]')
    dateindex_check = df.shape[1]

    assert dateindex_check == 1

def test_derivate_time_info():
    '''Test if this method is derivating correctly the time info with
    the correct names'''
    
    df = data_trans.derivate_time_info()
    test_cols = list(df.columns)
    cols_time_info = ['Year', 'Month', 'Week of Year', 
                        'Day of Month', 'Day of Week',
                        'Daily', 'Weekly', 'Monthly',
                        'Weekend']

    assert all(item in test_cols for item in cols_time_info)

def test_derivate_int_float_columns():
    '''Check if is just keeping columns "int64" or "float64"'''
    
    df = data_trans.derivate_int_float_columns()
    df1 = df.select_dtypes(include=['int64', 'float64'])

    return assert_frame_equal(df, df1)

def test_rescaling():
    '''Test rescaling options to know if it's not rescaling for a different
    from asked'''

    all_methods = ['box-cox', 'yeo-johnson', 'min-max', 'robust-scaler', 'log1p']

    for method in all_methods:
        tuple_df = list(df_test.select_dtypes(include=['int64', 'float64']).columns)
        y = choice(tuple(tuple_df))
        df, scaler = data_trans.rescaling(df=df_test, y=y, method=method)
        df1, scaler1 = data_trans.rescaling(df=df_test, y=y, method=method)

        return assert_frame_equal(df, df1)