import datetime as dt
import numpy as np
import pandas as pd
from   sklearn import preprocessing as pp

from resources.logger_msg import LoggerMsg

class DataTransform():

    def __init__(self, df: pd.DataFrame, date_col: str = 'nan', 
                start_date: str = '2020-01-01', 
                end_date: str = dt.datetime.now().strftime("%Y-%m-%d"), **kwargs):

        self.start_date = start_date
        self.end_date = end_date
        self.df = df.copy()
        self.date_col = date_col
        self.logger = LoggerMsg(file_name='DataTrans')

    def check_dateindex(self, **kwargs):
        '''Check if the index is datetimeindex'''

        df = self.df.copy()

        df['partner'] = 1
        df = df['partner'].reset_index(drop=False).select_dtypes('datetime64[ns]')
        date_index_check = df.shape[1]

        return date_index_check

    def transform_dateindex(self, date_index_check: int, **kwargs):
        '''Transform index to datetimeindex if it's not a datetimeindex yet using
        the column passed how date_col at the start of this class'''

        df = self.df.copy()

        if (self.date_col == 'nan') & (date_index_check == 0):
            self.logger.full_error(msg='''Is necessary one date info in index or 
                                          column to do time procedures!''')

        elif (self.date_col != 'nan') & (date_index_check == 0):
            df[self.date_col] = pd.to_datetime(df[self.date_col])
            df = df.set_index(self.date_col)    
        
        else:
            self.date_col = 'index'

        df = df[df.index.to_series().between(self.start_date, self.end_date)]

        return df
    
    def check_transform_dateindex(self, **kwargs):
        '''Run check and transform datetimeindex methods to check if exist some datetime index
        and if not transform the date_col to a datetimeindex format'''

        date_index_check = self.check_dateindex()
        df = self.transform_dateindex(date_index_check = date_index_check)

        return df

    def derivate_time_info(self, **kwargs):
        '''Derivate time information from the datetimeindex'''
        
        df = self.check_transform_dateindex()

        df['Year'] = df.index.year
        df['Month'] = df.index.month
        df['Week of Year'] = df.index.isocalendar().week
        df['Day of Month'] = df.index.day
        df['Day of Week']  = df.index.day_of_week
        df['Daily'] = df.index

        cols = [['Week of Year', 'Weekly'], ['Month', 'Monthly']]
        
        for c in cols: 
            df[c[0]] = df[c[0]].astype(int).apply(lambda x: '0' + str(x) if x < 10 else str(x))
            df['Year'] = df['Year'].astype(str)
            df[c[1]] = df['Year'] + df[c[0]]

        df['Year']  = df['Year'].astype(int)
        df['Month'] = df['Month'].astype(int)
        df['Week of Year']  = df['Week of Year'].astype(int)

        df['Weekend'] = df['Day of Week'].apply(lambda x: 
                                                1 if x in [5, 6] else 0)

        return df

    def derivate_int_float_columns(self, **kwargs):
        '''Filter dataset to just contain int64 and float64 columns'''

        date_index_check = self.check_dateindex()

        if (self.date_col == 'nan') & (date_index_check == 0):
            df = self.df.copy()
        else:
            df = self.check_transform_dateindex()
        
        num_attributes = df.select_dtypes(include=['int64', 'float64'])

        return num_attributes

    def rescaling(self, y: str, df: pd.DataFrame, method: str = 'yeo-johnson', **kwargs):
        '''Rescale the column passed as "y" to a scale who was passed in "method" attribute
        and check if this transformation is correct with the method "test_rescale"'''

        df = df.copy()

        if method in ['box-cox', 'yeo-johnson']:
            scaler = pp.PowerTransformer(method=method)
            scaler = scaler.fit(df[[y]])
            df[f'{method}_{y}'] = scaler.transform(df[[y]])
        elif method == 'min-max':
            scaler = pp.MinMaxScaler()
            scaler = scaler.fit(df[[y]])
            df[f'{method}_{y}'] = scaler.transform(df[[y]])
        elif method == 'robust-scaler':
            scaler = pp.RobustScaler()
            scaler = scaler.fit(df[[y]])
            df[f'{method}_{y}'] = scaler.transform(df[[y]])
        elif method == 'log1p':
            scaler = 'log1p'
            df[f'{method}_{y}'] = np.log1p(df[y])
        else:
            self.logger.needed_error(var = "Method", options="['box-cox', 'yeo-johnson', 'min-max', 'robust-scaler', 'log1p']")

        self.test_rescale(y=y, method=method, scaler=scaler, df=df)
        df = df.drop(y, axis=1)

        return df, scaler

    def inverse_transformation(self, df: pd.DataFrame, col_orig_name: str, y_nt: str, scaler, **kwargs):
        '''Undo the rescaling based in the scaler passed'''

        df = df.copy()
        df[f'{col_orig_name}'] = df[y_nt]
        df = df.drop(y_nt, axis=1)

        try:
            if scaler == 'log1p':
                df[f'{y_nt}_reversed'] = np.expm1(df[f'{col_orig_name}'])
            else:
                df[f'{y_nt}_reversed'] = scaler.inverse_transform(df[[f'{col_orig_name}']])
        except:
            self.logger.full_error("Check scaler passed!")

        return df.drop(col_orig_name, axis=1)

    def test_rescale(self, method: str, scaler, df: pd.DataFrame, y: str, **kwargs):
        '''Run test inverse transformation with the scale passed to guarantee that is
        possible to undo the transformation with no big differences'''

        df = df.copy()
        df['orig_col'] = df[y]
        df = self.inverse_transformation(df=df, col_orig_name=y, y_nt=f'{method}_{y}', scaler=scaler) 
        dif_nt = (df['orig_col'] - df[f'{method}_{y}_reversed']).mean()

        if dif_nt > 0.01:
            self.logger.generic_error(f"Nature Transformation ({method})")
        elif (dif_nt < 0.01) & (dif_nt > 0):
            self.logger.full_warning(f'''The mean difference in {method} transformation 
                                         is below 0.01! (difference = {dif_nt})''')

    def prepare_dataframe_timeseries(self, y: str, method: str = 'yeo-johnson', exogenous: list = False, **kwargs):
        '''Prepare the timeserie to the modeling process'''
        
        df = self.check_transform_dateindex()
        df, scaler = self.rescaling(df=df, y=y, method=method)
        df.index = pd.DatetimeIndex(df.index.values, freq=df.index.inferred_freq)

        if exogenous:
            exogenous.append(f'{method}_{y}')
            df = df[exogenous]            
        else:
            df = df[f'{method}_{y}']

        return df, scaler