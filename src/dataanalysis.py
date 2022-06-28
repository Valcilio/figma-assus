import dataframe_image as dfi
from importlib.resources import path
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import shutil
from statsmodels.tsa.seasonal import seasonal_decompose
from   statsmodels.tsa.stattools import adfuller

from datatransform import DataTransform
from resources.logger_msg import LoggerMsg

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
        self.logger = LoggerMsg(file_name='DataAnaly')

    def label_size_settings(self, **kwargs):
        '''Set label sizes when is just one figure'''
        
        plt.rc('axes',  labelsize=self.axes_size)
        plt.rc('xtick', labelsize=self.ticks_size)
        plt.rc('ytick', labelsize=self.ticks_size)

        return None

    def figure_size_settings(self, **kwargs):
        '''Set figure size when is just one figure'''

        plt.rc("figure", figsize=self.individual_figsize)

        return None
        
    def run_figure_sizes_settings(self, **kwargs):
        '''Set label and figure sizes when is just one figure'''

        self.label_size_settings()
        self.figure_size_settings()

        return None

    def save_fig(self, saving_figloc: path, df: pd.DataFrame = None, **kwargs):
        '''Save figure and dataframes in the given path'''

        if df is not None:
            fig_name = os.path.basename(saving_figloc)
            dfi.export(df, fig_name);
            shutil.move(fig_name, saving_figloc);

        else:
            plt.savefig(saving_figloc)

    def adfuller_writer(self, y: str, saving_txtloc: str, autolag: str = 'AIC', **kwargs):
        '''Write adfuller for stationary analysis in given path'''

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
        '''Read adfuller in given path'''

        with open(saving_txtloc) as adfuller:
            adfuller = print(adfuller.read())

        return adfuller

    def adfuller_description(self, y: str, saving_txtloc: str, **kwargs):
        '''Write and read adfuller for stationary analysis'''

        self.adfuller_writer(y=y, saving_txtloc=saving_txtloc)
        adfuller = self.adfuller_reader(saving_txtloc=saving_txtloc)

        return adfuller

    def statistical_description(self, saving_figloc: str = False, **kwargs):
        '''Calculate and show statistical descriptions'''

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
        '''Plot seasonal decomposer for stationary and stability time analysis'''

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
        '''Plot time stability'''

        df = self.derivate_time_info()

        df[x] = df[x].astype(str)
        df = df.groupby(x).median()
        df.plot(figsize=self.individual_figsize, title=f"{x}'s Stability", **kwargs)

        if saving_figloc:
            self.save_fig(saving_figloc=saving_figloc)

        return None

    def internal_timely_stability(self, x: str, y: str, ax_stab: matplotlib.axes.Axes = False, 
                                  **kwargs):
        '''It's just for internal use cases, plot time stability'''

        df = self.derivate_time_info()
        df[x] = df[x].astype(str)

        ax_stab.set_title(f"{x}'s Stability")
        df = df.groupby(x).median()
        df.plot(y=y, ax=ax_stab, **kwargs)

        return None

    def all_timely_stability(self, y, all_figsize: tuple = (22,15), saving_figloc: path = False, **kwargs):
        '''Concat four figures with different parts of time stability to plot'''

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=all_figsize);

        self.internal_timely_stability(x='Daily', y=y, ax_stab=ax1, **kwargs);
        self.internal_timely_stability(x='Weekly', y=y, ax_stab=ax2, **kwargs);
        self.internal_timely_stability(x='Monthly', y=y, ax_stab=ax3, **kwargs);
        self.internal_timely_stability(x='Year', y=y, ax_stab=ax4, **kwargs);

        if saving_figloc:
            self.save_fig(saving_figloc=saving_figloc)

        return None

    def outlier_detector_boxplot(self, x: str, saving_figloc: path = False, **kwargs):
        '''Plot boxplot, it's idealized to detect outliers in temporal situations'''

        df = self.derivate_time_info()
 
        self.run_figure_sizes_settings()
        plt.title(f"{x}'s Boxplot to Outlier Detection", fontsize=self.titlesize)

        sns.boxplot(data=df, x=x, **kwargs)

        if saving_figloc:
            self.save_fig(saving_figloc=saving_figloc)

        return None

    def internal_outlier_detector_boxplot(self, x: str, ax_box: matplotlib.axes.Axes, **kwargs):
        '''It's just for internal use cases, plot boxplot to outlier detection'''

        df = self.derivate_time_info()

        ax_box.set_title(f"{x}'s Boxplot to Outlier Detection")

        if len(df[x].unique()) >= 13:
            ax_box.set_xticks(df[x])
            ax_box.set_xticklabels(df[x], rotation=70)

        sns.boxplot(data=df, x=x, ax=ax_box, **kwargs);

        return None

    def all_temporal_outlier_detector_boxplots(self, y: str, all_figsize: tuple =(22, 20), saving_figloc: path = False, **kwargs):
        '''Plot six boxplot to temporal outlier detector'''

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
        '''Plot distribution to check the type of from all the numerical variables in dataset'''

        df = self.derivate_int_float_columns()
        df.hist(figsize=all_figsize, **kwargs);

        if saving_figloc:
            self.save_fig(saving_figloc=saving_figloc)

        return None

    def internal_distribution_check(self, df: pd.DataFrame, ax_dist: matplotlib.axes.Axes, 
                                    y_res: str, **kwarg):
            '''It's just for internal use cases, plot distribution of one variable'''

            var_name = y_res.title()
            ax_dist.set_title(f"{var_name}'s Distribution")
            df[y_res].hist(ax=ax_dist)

            return None

    def internal_rescaling_distribution_check(self, df: pd.DataFrame, ax_dist: matplotlib.axes.Axes, 
                                    y_res: str, method: str, **kwarg):
        '''It's just for internal use cases, plot distribution check with rescalling effect to 
        check how transform the dataframe for understand who is the most effective transformation
        in a good way'''
        
        var_name = y_res.title()
        method_name = method.replace('-', ' ').title().replace(' ', '-')
        ax_dist.set_title(f"{var_name}'s Distribution with Rescaled By {method_name}")
        df, scale = self.rescaling(df=df, y=y_res, method=method)
        df[f'{method}_{y_res}'].hist(ax=ax_dist)

        return None

    def rescalling_effect_check(self, y: str, all_figsize: tuple =(14, 9), saving_figloc: path = False, **kwargs):
        '''Plot four distributions with differents data formats to understand who is
        the best transformation to use in modeling or analysis cases'''

        df = self.derivate_int_float_columns()
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=all_figsize);

        self.internal_distribution_check(df=df, y_res=y, ax_dist=ax1)
        self.internal_rescaling_distribution_check(df=df, y_res=y, ax_dist=ax2, method='log1p')
        self.internal_rescaling_distribution_check(df=df, y_res=y, ax_dist=ax3, method='box-cox')
        self.internal_rescaling_distribution_check(df=df, y_res=y, ax_dist=ax4, method='yeo-johnson')

        if saving_figloc:
            self.save_fig(saving_figloc=saving_figloc)

        return None