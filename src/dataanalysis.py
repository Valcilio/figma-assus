import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from logger.logger_msg import LoggerMsg

class  DataAnalysis():

    def __init__(self, df: pd.DataFrame, date_col = 'nan', 
                individual_figsize = (18,8),
                titlesize=20, axes_size = 18, ticks_size = 13,
                start_date = '2020-01-01', end_date='2022-12-31', **kwargs):

        self.df = df
        self.date_col = date_col
        self.individual_figsize = individual_figsize
        self.titlesize = titlesize
        self.axes_size = axes_size
        self.ticks_size = ticks_size
        self.start_date = start_date
        self.end_date = end_date
        self.logger = LoggerMsg(file_name='Data Analysis')

    def label_size_settings(self, **kwargs):
        
        plt.rc('axes',  labelsize=self.axes_size)
        plt.rc('xtick', labelsize=self.ticks_size)
        plt.rc('ytick', labelsize=self.ticks_size)

        return None

    def figure_size_settings(self, **kwargs):

        plt.figure(figsize=self.individual_figsize)

        return None
        
    def run_figure_sizes_settings(self, **kwargs):

        self.label_size_settings()
        self.figure_size_settings()

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

        df['Week of Year'] = df.index.isocalendar().week
        df['Day of Month'] = df.index.day
        df['Day of Week']  = df.index.day_of_week
        df['Daily'] = df.index

        cols = [['Week of Year', 'Weekly'], ['Month', 'Monthly']]
        
        for c in cols: 
            df[c[0]] = df.index.month
            df[c[0]] = df[c[0]].astype(int).apply(lambda x: '0' + str(x) if x < 10 else str(x))
            df['Year'] = df.index.year
            df['Year'] = df['Year'].astype(str)
            df[c[1]] = df['Year'] + df[c[0]]

        df['Year']  = df['Year'].astype(int)
        df['Month'] = df['Month'].astype(int)
        df['Week of Year']  = df['Week of Year'].astype(int)

        df['Weekend'] = df['Day of Week'].apply(lambda x: 
                                                1 if x in [5, 6] else 0)

        df = df[df.index.to_series().between(self.start_date, self.end_date)]

        return df

    def derivate_int_float_columns(self, **kwargs):

        df = self.df.copy()
        num_attributes = df.select_dtypes(include=['int64', 'float64'])

        return num_attributes

    def statistical_description(self, **kwargs):

        df = self.derivate_int_float_columns()

        ct1 = pd.DataFrame(df.apply(np.mean)).T
        ct2 = pd.DataFrame(df.apply(np.median)).T

        d1 = pd.DataFrame(df.apply(np.std)).T
        d2 = pd.DataFrame(df.apply(min)).T
        d3 = pd.DataFrame(df.apply(max)).T
        d4 = pd.DataFrame(df.apply(lambda x: x.max() - x.min())).T
        d5 = pd.DataFrame(df.apply(lambda x: x.skew())).T
        d6 = pd.DataFrame(df.apply(lambda x: x.kurtosis())).T

        m = pd.concat([ct1, ct2, d1, d2, d3, d4, d5, d6]).T.reset_index()
        m.columns = ['attributes', 'mean', 'median', 'std', 
                     'min', 'max', 'range', 'skew', 'kurtosis']

        return m

    def timely_stability(self, last_days = 90, x = 'Daily', **kwargs):

        df = self.derivate_time_info()

        if x == 'Daily':
            df = df.tail(last_days)
            df.plot(**kwargs, figsize=self.individual_figsize, title=f"{x}'s Time Stability")

        else:
            df[x] = df[x].astype(str)
            df = df.groupby(x).median()
            df.plot(**kwargs, figsize=self.individual_figsize, title=f"{x}'s Time Stability")

        return None

    def internal_timely_stability(self, x: str, y: str, ax, last_days = 90, **kwargs):

        df = self.derivate_time_info()
        df[x] = df[x].astype(str)
        df = df.groupby(x).median()

        if x == 'Daily':
            df.tail(last_days).plot(y=y, ax=ax)

        else:
            df.plot(y=y, ax=ax)

        return None

    def all_timely_stability(self, y, all_figsize=(22,15), **kwargs):

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=all_figsize);

        ax1_var = 'Year'
        ax1.set_title(f"{ax1_var}'s Stability")
        self.internal_timely_stability(x=ax1_var, y=y, ax=ax1, **kwargs);

        ax2_var = 'Monthly'
        ax2.set_title(f"{ax2_var}'s Stability")
        self.internal_timely_stability(x=ax2_var, y=y, ax=ax2, **kwargs);

        ax3_var = 'Weekly'
        ax3.set_xticklabels('xtick', rotation=70)
        ax3.set_title(f"{ax3_var}'s Stability")
        self.internal_timely_stability(x=ax3_var, y=y, ax=ax3, **kwargs);

        ax4_var = 'Daily'
        ax4.set_xticklabels('xtick', rotation=70)
        ax4.set_title(f"{ax4_var}'s Stability")
        self.internal_timely_stability(x=ax4_var, y=y, ax=ax4, **kwargs);

        return None

    def outlier_detector_boxplot(self, x: str, settings_title=True, **kwargs):
  
        df = self.derivate_time_info()

        if settings_title:
            self.run_figure_sizes_settings()
            plt.title(f"{x}'s Boxplot to Outlier Detection", fontsize=self.titlesize)

        sns.boxplot(data=df, x=x, **kwargs);

        return None

    def all_temporal_outlier_detector_boxplots(self, all_figsize=(22, 20), **kwargs):

        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=all_figsize);

        ax1_var = 'Year'
        ax1.set_title(f"{ax1_var}'s Boxplot to Outlier Detection")
        self.outlier_detector_boxplot(x=ax1_var, y='close', settings_title=False, ax=ax1);

        ax2_var = 'Month'
        ax2.set_title(f"{ax2_var}'s Boxplot to Outlier Detection")
        self.outlier_detector_boxplot(x=ax2_var, y='close', settings_title=False, ax=ax2);

        ax3_var = 'Week of Year'
        ax3.set_xticklabels('xtick', rotation=70)
        ax3.set_title(f"{ax3_var}'s Boxplot to Outlier Detection")
        self.outlier_detector_boxplot(x=ax3_var, y='close', settings_title=False, ax=ax3);

        ax4_var = 'Weekend'
        ax4.set_title(f"{ax4_var}'s Boxplot to Outlier Detection")
        self.outlier_detector_boxplot(x=ax4_var, y='close', settings_title=False, ax=ax4);

        ax5_var = 'Day of Month'
        ax5.set_title(f"{ax5_var}'s Boxplot to Outlier Detection")
        self.outlier_detector_boxplot(x=ax5_var, y='close', settings_title=False, ax=ax5);

        ax6_var = 'Day of Week'
        ax6.set_title(f"{ax6_var}'s Boxplot to Outlier Detection")
        self.outlier_detector_boxplot(x=ax6_var, y='close', settings_title=False, ax=ax6);

        return None

    def distribution_check(self, all_figsize=(22,15), **kwargs):

        df = self.derivate_int_float_columns()

        df.hist(figsize=all_figsize, **kwargs);

        return None