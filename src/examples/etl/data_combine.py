import pandas as pd
import datetime as dt
from pandas.core.frame import DataFrame


class DataCombine():
    
    def __init__(self, save_path_final: str, df_santander: DataFrame, df_bacen: DataFrame, **kwargs):
        self.today = dt.datetime.now().strftime('%Y%m%d%H')
        self.save_path_final = save_path_final
        self.df_santander = df_santander.copy()
        self.df_bacen     = df_bacen.copy()
    
    def run(self, **kwargs):
        # copiando dataframes
        df_santander = self.df_santander
        df_bacen     = self.df_bacen

        # derivando ano
        df_santander['year'] = df_santander['date'].dt.year
        df_santander['month'] = df_santander['date'].dt.month

        # concat dataframes
        df_total = pd.merge(df_bacen, df_santander, how='left', on=['year', 'month'])

        # dropping columns
        df_total = df_total.drop(['year', 'month', 'date_y'], axis=1).rename(columns={'date_x':'date'})

        # salvando dataframe atualizado
        df_total.to_csv(rf'{self.save_path_final}/indicadores_{self.today}.csv', index=False)

        return df_total