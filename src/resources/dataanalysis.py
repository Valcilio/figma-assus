import dataframe_image as dfi
from importlib.resources import path
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import shutil
from   sklearn.preprocessing import PowerTransformer
from statsmodels.tsa.seasonal import seasonal_decompose
from   statsmodels.tsa.stattools import adfuller

from .datatransform import DataTransform
from .logger_msg import LoggerMsg

class  DataAnalysis(DataTransform):

    def __init__(self, df: pd.DataFrame, date_col = 'nan', 
                individual_figsize = (18,8),
                titlesize=20, axes_size = 13, ticks_size = 10,
                start_date = '2020-01-01', end_date='2022-12-31', **kwargs):
        
        super().__init__(df, date_col, start_date, end_date)

        self.individual_figsize = individual_figsize
        self.titlesize = titlesize
        self.axes_size = axes_size
        self.ticks_size = ticks_size
        self.logger = LoggerMsg(file_name='Data Analysis')

    def label_size_settings(self, **kwargs):
        
        plt.rc('axes',  labelsize=self.axes_size)
        plt.rc('xtick', labelsize=self.ticks_size)
        plt.rc('ytick', labelsize=self.ticks_size)

        return None

    def figure_size_settings(self, **kwargs):

        plt.rc("figure", figsize=self.individual_figsize)

        return None
        
    def run_figure_sizes_settings(self, **kwargs):

        self.label_size_settings()
        self.figure_size_settings()

        return None

    def save_fig(self, saving_figloc: path, df: pd.DataFrame = None, **kwargs):

        if df is not None:
            fig_name = os.path.basename(saving_figloc)
            dfi.export(df, fig_name);
            shutil.move(fig_name, saving_figloc);

        else:
            plt.savefig(saving_figloc)

    def adfuller_writer(self, y: str, saving_txtloc: str, autolag: str = 'AIC', **kwargs):

        df = self.check_transform_dateindex()
        df = adfuller(df[y], autolag = autolag, **kwargs)

        with open(saving_txtloc, 'w+') as adf:
            print(f"1. ADF : {df[0]}", file=adf)
            print(f"2. P-Value : {df[1]}", file=adf)
            print(f"3. Num Of Lags : {df[2]}", file=adf)
            print(f"4. Num Of Observations Used For ADF Regression and Critical Values Calculation: {df[3]}", file=adf)
            print(f"5. Critical Values :", file=adf)
            for key, val in df[4].items():
                print(f"\t{key}: {val}", file=adf)
            adf.close()

        return None

    def adfuller_reader(self, saving_txtloc: str, **kwargs):

        with open(saving_txtloc) as adfuller:
            adfuller = print(adfuller.read())

        return adfuller

    def adfuller_description(self, y: str, saving_txtloc: str, **kwargs):

        self.adfuller_writer(y=y, saving_txtloc=saving_txtloc)
        adfuller = self.adfuller_reader(saving_txtloc=saving_txtloc)

        return adfuller

    def statistical_description(self, saving_figloc: str = False, **kwargs):

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

        if saving_figloc:
            self.save_fig(df = m, saving_figloc=saving_figloc)

        return m

    def plot_seasonal_decomposer(self, y: str, all_inches: tuple = (20, 10), model: str = 'additive', saving_figloc: str = False, **kwargs):
        
        df = self.check_transform_dateindex()
        self.label_size_settings()
        fig = seasonal_decompose(df[y], model=model)

        fig_plot = fig.plot();
        fig_plot.set_size_inches(all_inches)
        fig_plot

        if saving_figloc:
            fig_plot.savefig(saving_figloc)

        return None

    def timely_stability(self, x: str, saving_figloc: path = False, **kwargs):

        df = self.derivate_time_info()

        df[x] = df[x].astype(str)
        df = df.groupby(x).median()
        df.plot(figsize=self.individual_figsize, title=f"{x}'s Stability", **kwargs)

        if saving_figloc:
            self.save_fig(saving_figloc=saving_figloc)

        return None

    def internal_timely_stability(self, x: str, y: str, ax_stab: matplotlib.axes.Axes = False, 
                                  **kwargs):

        df = self.derivate_time_info()
        df[x] = df[x].astype(str)

        ax_stab.set_title(f"{x}'s Stability")
        df = df.groupby(x).median()
        df.plot(y=y, ax=ax_stab, **kwargs)

        return None

    def all_timely_stability(self, y, all_figsize: tuple = (22,15), saving_figloc: path = False, **kwargs):

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=all_figsize);

        self.internal_timely_stability(x='Daily', y=y, ax_stab=ax1, **kwargs);
        self.internal_timely_stability(x='Weekly', y=y, ax_stab=ax2, **kwargs);
        self.internal_timely_stability(x='Monthly', y=y, ax_stab=ax3, **kwargs);
        self.internal_timely_stability(x='Year', y=y, ax_stab=ax4, **kwargs);

        if saving_figloc:
            self.save_fig(saving_figloc=saving_figloc)

        return None

    def outlier_detector_boxplot(self, x: str, saving_figloc: path = False, **kwargs):
  
        df = self.derivate_time_info()
 
        self.run_figure_sizes_settings()
        plt.title(f"{x}'s Boxplot to Outlier Detection", fontsize=self.titlesize)

        sns.boxplot(data=df, x=x, **kwargs)

        if saving_figloc:
            self.save_fig(saving_figloc=saving_figloc)

        return None

    def internal_outlier_detector_boxplot(self, x: str, ax_box: matplotlib.axes.Axes = False, **kwargs):
 
        df = self.derivate_time_info()

        ax_box.set_title(f"{x}'s Boxplot to Outlier Detection")

        if len(df[x].unique()) >= 13:
            ax_box.set_xticks(df[x])
            ax_box.set_xticklabels(df[x], rotation=70)

        sns.boxplot(data=df, x=x, ax=ax_box, **kwargs);

        return None

    def all_temporal_outlier_detector_boxplots(self, y: str, all_figsize: tuple =(22, 20), saving_figloc: path = False, **kwargs):

        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=all_figsize);

        self.internal_outlier_detector_boxplot(x='Year',         ax_box=ax1, y=y);
        self.internal_outlier_detector_boxplot(x='Month',        ax_box=ax2, y=y);
        self.internal_outlier_detector_boxplot(x='Week of Year', ax_box=ax3, y=y);
        self.internal_outlier_detector_boxplot(x='Weekend',      ax_box=ax4, y=y);
        self.internal_outlier_detector_boxplot(x='Day of Month', ax_box=ax5, y=y);
        self.internal_outlier_detector_boxplot(x='Day of Week',  ax_box=ax6, y=y);

        if saving_figloc:
            self.save_fig(saving_figloc=saving_figloc)

        return None

    def distribution_check(self, all_figsize: tuple =(22,15), saving_figloc: path = False, **kwargs):

        df = self.derivate_int_float_columns()
        df.hist(figsize=all_figsize, **kwargs);

        if saving_figloc:
            self.save_fig(saving_figloc=saving_figloc)

        return None

    def nature_transform_effect_check(self, y: str, all_figsize: tuple =(14, 9), saving_figloc: path = False, **kwargs):

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

        if saving_figloc:
            self.save_fig(saving_figloc=saving_figloc)

        return None