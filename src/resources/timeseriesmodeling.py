import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings

from .datatransform import DataTransform
from .logger_msg import LoggerMsg

class TimeSeriesModeling(DataTransform):

    def __init__(self, df: pd.DataFrame, **kwargs):

        self.df = df.copy()
        self.logger = LoggerMsg('TSModel')

    def fit_sarimax(self, **kwargs):
        '''Fit sarimax model'''

        warnings.filterwarnings("ignore")
        model=SARIMAX(self.df, order=(2,1,5), seasonal_order=(1, 1, 1, 24))
        self.fitted_model = model.fit(disp=0)

        return self.fitted_model

    def forecast(self, fitted_model = False, next_days: int = 15, **kwargs):
        '''Use fitted model to forecasting. If don't has any fitted model
        passed, will use some model in the class, if don't exist too, will
        raise a error saying that is needed a fitted model to predict'''
        
        try:
            if fitted_model:
                df_forecast = pd.DataFrame(fitted_model.predict(start=len(self.df), end=len(self.df) + next_days, dynamic=True))
            else:
                df_forecast = pd.DataFrame(self.fitted_model.predict(start=len(self.df), end=len(self.df) + next_days, dynamic=True))
        except:
            self.logger.full_error("Call a 'fit_' method before this or pass a time series fitted model!")
        df_result = pd.concat([self.df, df_forecast], axis=1).rename(columns={'predicted_mean':f'{self.df.name}_forecast'})
        
        return df_result
    