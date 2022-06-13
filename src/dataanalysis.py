import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from logger.logger_msg import LoggerMsg

class  DataAnalysis():

    def __init__(self, df: pd.DataFrame, date_col = 'nan', **kwargs):
        self.df = df
        self.date_col = date_col
        self.logger = LoggerMsg(file_name='Data Analysis')

    def transform_date_col(self, **kwargs):
        
        df = self.df.copy()
        df1 = self.df.copy()

        df1['partner'] = 1
        df1 = df1['partner'].reset_index(drop=False).select_dtypes('datetime64[ns]')
        date_index_check = df1.shape[1]

        if (self.date_col == 'nan') & (date_index_check != 1):
            self.logger.full_error(msg='''Is necessary one date info in index or 
                                          column to plot stability!''')

        elif (self.date_col != 'nan') & (date_index_check == 0):
            df[self.date_col] = pd.to_datetime(df[self.date_col])
            df = df.set_index(self.date_col)
        
        elif (date_index_check == 1):
            None

        return df

    def statistical_description(self, **kwargs):

        df = self.df.copy()

        num_attributes = df.select_dtypes(include=['int64', 'float64'])

        # Central Tendency - mean, median
        ct1 = pd.DataFrame(num_attributes.apply(np.mean)).T
        ct2 = pd.DataFrame(num_attributes.apply(np.median)).T

        # Dispersion - std, min, max, range, knew, kurtosis
        d1 = pd.DataFrame(num_attributes.apply(np.std)).T
        d2 = pd.DataFrame(num_attributes.apply(min)).T
        d3 = pd.DataFrame(num_attributes.apply(max)).T
        d4 = pd.DataFrame(num_attributes.apply(lambda x: x.max() - x.min())).T
        d5 = pd.DataFrame(num_attributes.apply(lambda x: x.skew())).T
        d6 = pd.DataFrame(num_attributes.apply(lambda x: x.kurtosis())).T

        # concatenate
        m = pd.concat([ct1, ct2, d1, d2, d3, d4, d5, d6]).T.reset_index()
        m.columns = ['attributes', 'mean', 'median', 'std', 
                     'min', 'max', 'range', 'skew', 'kurtosis']

        return m

    def daily_stability(self, last_days: int, **kwargs):

        df = self.transform_date_col().tail(last_days)

        df.plot(**kwargs)

        return None
    
    def monthly_stability(self, **kwargs):

        df = self.transform_date_col()

        df['month'] = df.index.month
        df['month'] = df['month'].astype(int).apply(lambda x: '0' + str(x) if x < 10 else str(x))

        df['year'] = df.index.year
        df['year'] = df['year'].astype(str)

        df['monthly'] = df['year'] + df['month']

        df = df.groupby('monthly').median()[:-1]

        df.plot(**kwargs)

        return None

    def annual_stability(self, **kwargs):

        df = self.transform_date_col()

        df['year'] = df.index.year
        df['year'] = df['year'].astype(str)
        df = df.groupby('year').median()

        df.plot(**kwargs)

        return None
