import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn import metrics as m
import warnings

from datatransform import DataTransform
from resources.logger_msg import LoggerMsg

class TimeSeriesModeling(DataTransform):

    def __init__(self, df: pd.DataFrame, **kwargs):

        super().__init__(df=df)

        self.df = df.copy()
        self.logger = LoggerMsg('TSModel')

    def internal_reverse_scale(self, df: pd.DataFrame, orig_name:str, scaler=False, **kwargs):
        '''Reverse scale for results from forecating'''

        warnings.filterwarnings("ignore")
        cols = list(df.columns)
        if scaler:
            for c in cols:
                df.loc[:, c] = self.inverse_transformation(df=df, y_nt=c, col_orig_name=orig_name, scaler=scaler).loc[: ,c + '_reversed'].copy()

    def fit_sarimax(self, passed_order: tuple = (2, 1, 5), seas_order: tuple = (1, 1, 1, 24), **kwargs):
        '''Fit sarimax model'''

        warnings.filterwarnings("ignore")
        model=SARIMAX(self.df, order=passed_order, seasonal_order=seas_order, **kwargs)
        self.fitted_model = model.fit(disp=0)

        return self.fitted_model

    def forecast(self, base_days: int = 'no value passed', fitted_model = False, old_days: int = 0, next_days: int = 15, **kwargs):
        '''Use fitted model to forecasting. If don't has any fitted model
        passed, will use some model in the class, if don't exist too, will
        raise a error saying that is needed a fitted model to predict'''

        if base_days == 'no value passed':
            base_days = len(self.df)
        
        try:
            if fitted_model:
                df_forecast = pd.DataFrame(fitted_model.predict(start=base_days + old_days, end=base_days
                                                                + next_days, dynamic=True), **kwargs)
            else:
                df_forecast = pd.DataFrame(self.fitted_model.predict(start=base_days + old_days, end=base_days
                                                                     + next_days, dynamic=True), **kwargs)
        except:
            self.logger.full_error("Call a 'fit_' method before this or pass a time series fitted model!")
        self.df_result = pd.concat([self.df, df_forecast], axis=1).rename(columns={'predicted_mean':f'{self.df.name}_forecast'})
        
        return self.df_result

    def model_summary(self, fitted_model = False, **kwargs):
        if fitted_model:
            return fitted_model.summary()
        else:
            return self.fitted_model.summary()

    def model_performance(self, model_name: str, y: pd.Series, yhat: pd.Series, **kwargs):
        '''Calculate metrics of modeling to judge the model's peformance'''
            
        mae = m.mean_absolute_error(y, yhat)
        mape = m.mean_absolute_percentage_error(y, yhat)
        rmse = np.sqrt(m.mean_squared_error(y, yhat))
        
        return pd.DataFrame({'Model Name': model_name,
                            'MAE': mae,
                            'MAPE': mape,
                            'RMSE': rmse}, index=[0])

    def rolling_cross_validation(self, orig_name: str, fitted_model = False, validations:int = 7, 
                                 num_of_nexts:int = 30, model_name: str = 'SARIMAX', 
                                 scaler = False, **kwargs):
        '''Calculate metrics of modeling to judge the model's performance through a reality simulation (Cross Validation)'''

        mae_list = []
        mape_list = []
        rmse_list = []

        for i in reversed(range(1, validations+1, 1)):
            old_days = int(len(self.df)/i)
            next_days = int(len(self.df)/i) + num_of_nexts
            if next_days > len(self.df):
                break

            df_result = self.forecast(fitted_model=fitted_model, base_days=0, old_days=old_days, next_days=next_days)
            df_result = df_result.dropna()
            self.internal_reverse_scale(df=df_result, orig_name=orig_name, scaler=scaler)
            
            m_result = self.model_performance(model_name, df_result.iloc[:, 1], df_result.iloc[:, 0], orig_name=orig_name)
            mae_list.append(m_result['MAE'])
            mape_list.append(m_result['MAPE'])
            rmse_list.append(m_result['RMSE'])

        return pd.DataFrame( [{
                          'Model Name': model_name,
                          'MAE CV': int(np.mean( mae_list )),
                          'MAPE CV': np.mean( mape_list ),
                          'RMSE CV': np.mean( rmse_list )}])