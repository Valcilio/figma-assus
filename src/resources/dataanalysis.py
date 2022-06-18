import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
from   sklearn.preprocessing import PowerTransformer
import sys
sys.path.insert(0, os.environ.get('SRC_FIGMA_PATH'))

from resources.logger.logger_msg import LoggerMsg

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

    def timely_stability(self, x: str, **kwargs):

        df = self.derivate_time_info()

        df[x] = df[x].astype(str)
        df = df.groupby(x).median()
        df.plot(figsize=self.individual_figsize, title=f"{x}'s Stability", **kwargs)

        return None

    def internal_timely_stability(self, x: str, y: str, ax_stab: matplotlib.axes.Axes = False, **kwargs):

        df = self.derivate_time_info()
        df[x] = df[x].astype(str)

        ax_stab.set_title(f"{x}'s Stability")
        df = df.groupby(x).median()
        df.plot(y=y, ax=ax_stab, **kwargs)

        return None

    def all_timely_stability(self, y, all_figsize=(22,15), **kwargs):

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=all_figsize);

        self.internal_timely_stability(x='Daily', y=y, ax_stab=ax1, **kwargs);
        self.internal_timely_stability(x='Weekly', y=y, ax_stab=ax2, **kwargs);
        self.internal_timely_stability(x='Monthly', y=y, ax_stab=ax3, **kwargs);
        self.internal_timely_stability(x='Year', y=y, ax_stab=ax4, **kwargs);

        return None

    def outlier_detector_boxplot(self, x: str, ax_box: matplotlib.axes.Axes = False, **kwargs):
  
        df = self.derivate_time_info()
 
        self.run_figure_sizes_settings()
        plt.title(f"{x}'s Boxplot to Outlier Detection", fontsize=self.titlesize)

        sns.boxplot(data=df, x=x, **kwargs)

        return None

    def internal_outlier_detector_boxplot(self, x: str, ax_box: matplotlib.axes.Axes = False, **kwargs):
 
        df = self.derivate_time_info()

        ax_box.set_title(f"{x}'s Boxplot to Outlier Detection")

        if len(df[x].unique()) >= 13:
            ax_box.set_xticks(df[x])
            ax_box.set_xticklabels(df[x], rotation=70)

        sns.boxplot(data=df, x=x, ax=ax_box, **kwargs);

        return None

    def all_temporal_outlier_detector_boxplots(self, y:str, all_figsize=(22, 20), **kwargs):

        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=all_figsize);

        self.internal_outlier_detector_boxplot(x='Year',         ax_box=ax1, y=y);
        self.internal_outlier_detector_boxplot(x='Month',        ax_box=ax2, y=y);
        self.internal_outlier_detector_boxplot(x='Week of Year', ax_box=ax3, y=y);
        self.internal_outlier_detector_boxplot(x='Weekend',      ax_box=ax4, y=y);
        self.internal_outlier_detector_boxplot(x='Day of Month', ax_box=ax5, y=y);
        self.internal_outlier_detector_boxplot(x='Day of Week',  ax_box=ax6, y=y);

        return None

    def distribution_check(self, all_figsize=(22,15), **kwargs):

        df = self.derivate_int_float_columns()
        df.hist(figsize=all_figsize, **kwargs);

        return None

    def nature_transform_effect_check(self, y: str, all_figsize=(14, 9), **kwargs):

        df = self.derivate_int_float_columns()
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=all_figsize);
        ax_var = y.capitalize()

        ax1.set_title(f"{ax_var}'s Distribution")
        df[y].hist(ax=ax1)

        ax2.set_title(f"{ax_var}'s Distribution with Nature Transformion By Log1p")
        df[f'{y}_log1p'] = np.log1p(df[y])
        df[f'{y}_log1p'].hist(ax=ax2)

        ax3.set_title(f"{ax_var}'s Distribution with Nature Transformion By Box-Cox")
        boxcox_scaler = PowerTransformer(method='box-cox')
        boxcox_scaler = boxcox_scaler.fit(df[[y]])
        df[f'{y}_box-cox'] = boxcox_scaler.transform(df[[y]])
        df[f'{y}_box-cox'].hist(ax=ax3)

        ax4.set_title(f"{ax_var}'s Distribution with Nature Transformion By Yeo-Johnson")
        yeojohnson_scaler = PowerTransformer(method='yeo-johnson')
        yeojohnson_scaler = yeojohnson_scaler.fit(df[[y]])
        df[f'{y}_yeo-johnson'] = yeojohnson_scaler.transform(df[[y]])
        df[f'{y}_yeo-johnson'].hist(ax=ax4)

        return None