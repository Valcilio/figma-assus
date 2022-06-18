import os
import pandas as pd
import sys
sys.path.insert(0, os.environ.get('SRC_FIGMA_PATH'))

from resources.logger.logger_msg import LoggerMsg

class DataTransform():

    def __init__(self, df: pd.DataFrame, date_col = 'nan', 
                start_date = '2020-01-01', end_date='2022-12-31', **kwargs):

        self.df = df
        self.date_col = date_col
        self.start_date = start_date
        self.end_date = end_date
        self.logger = LoggerMsg(file_name='Data Transform')

    def check_transform_dateindex(self, **kwargs):
        
        df = self.df.copy()
        df1 = self.df.copy()

        df1['partner'] = 1
        df1 = df1['partner'].reset_index(drop=False).select_dtypes('datetime64[ns]')
        date_index_check = df1.shape[1]

        if (self.date_col == 'nan') & (date_index_check != 1):
            self.logger.full_error(msg='''Is necessary one date info in index or 
                                          column to do time procedures!''')

        elif (self.date_col != 'nan') & (date_index_check == 0):
            df[self.date_col] = pd.to_datetime(df[self.date_col])
            df = df.set_index(self.date_col)
        
        elif (date_index_check == 1):
            None

        return df

    def derivate_time_info(self, **kwargs):
        
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

        df = df[df.index.to_series().between(self.start_date, self.end_date)].reset_index()

        return df

    def derivate_int_float_columns(self, **kwargs):

        df = self.df.copy()
        num_attributes = df.select_dtypes(include=['int64', 'float64'])

        return num_attributes