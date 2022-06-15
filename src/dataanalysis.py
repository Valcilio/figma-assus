import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from logger.logger_msg import LoggerMsg

class  DataAnalysis():

    def __init__(self, df: pd.DataFrame, date_col = 'nan', 
                figsize = (24,8), axes_size = 18, ticks_size = 13, 
                start_safra = '202101', end_safra='202206', **kwargs):

        self.df = df
        self.date_col = date_col
        self.figsize = figsize
        self.axes_size = axes_size
        self.ticks_size = ticks_size
        self.start_safra = start_safra
        self.end_safra = end_safra
        self.logger = LoggerMsg(file_name='Data Analysis')

    def figure_size_settings(self, **kwargs):

        plt.figure(figsize=self.figsize)
        plt.rc('axes',  labelsize=self.axes_size)
        plt.rc('xtick', labelsize=self.ticks_size)
        plt.rc('ytick', labelsize=self.ticks_size)

        return None

    def check_transform_datecol(self, **kwargs):
        
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
        
        df = self.check_transform_datecol()
        df['month'] = df.index.month
        df['month'] = df['month'].astype(int).apply(lambda x: '0' + str(x) if x < 10 else str(x))

        df['year'] = df.index.year
        df['year'] = df['year'].astype(str)

        df['Safra'] = df['year'] + df['month']

        df['Month']        = df['month'].astype(int)
        df['Year']         = df['year'].astype(int)
        df['Day of Month'] = df.index.day
        df['Day of Week']  = df.index.day_of_week

        df = df.drop(['month', 'year'], axis=1)

        df = df[(df['Safra'] >= self.start_safra) & (df['Safra'] <= self.end_safra)]

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

        df = self.check_transform_datecol().tail(last_days)

        df.plot(**kwargs)

        return None
    
    def monthly_stability(self, **kwargs):

        df = self.check_transform_datecol()

        df['month'] = df.index.month
        df['month'] = df['month'].astype(int).apply(lambda x: '0' + str(x) if x < 10 else str(x))

        df['year'] = df.index.year
        df['year'] = df['year'].astype(str)

        df['monthly'] = df['year'] + df['month']

        df = df.groupby('monthly').median()[:-1]

        df.plot(**kwargs)

        return None

    def annual_stability(self, **kwargs):

        df = self.check_transform_datecol()

        df['year'] = df.index.year
        df['year'] = df['year'].astype(str)
        df = df.groupby('year').median()

        df.plot(**kwargs)

        return None

    def outlier_analysis_boxplot(self, x: str, titlesize=20, **kwargs):
        
        temporal_information_list = ['Year', 'Month', 'Day of Month', 'Day of Week']

        if x not in temporal_information_list:
            self.logger.full_error(f"The 'x' column needs to be one in the following list {temporal_information_list}!")

        df = self.derivate_time_info()
        self.figure_size_settings()
        
        plt.title(f"{x}'s Boxplot to Outlier Detection", fontsize=titlesize)
        sns.boxplot(data=df, x=x, **kwargs);

        return None