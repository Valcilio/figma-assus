import datetime as dt
import inflection 
import openpyxl as ol
import pandas as pd
from logger.logger_msg import LoggerMSG

class SantanderETL():

    def __init__(self, excel_path: str, save_path: str,  **kwargs):
        self.excel_path = excel_path
        self.save_path = save_path
        self.today = dt.datetime.now().strftime('%Y%m%d%H')
        self.lm = LoggerMSG()

    # limpeza do csv
    def run(self, **kwargs):
        # chamando funções
        self.excel_clean()
        self.load_csv()
        self.rename_columns_csv()
        self.changing_dtypes()

        return self.df_santander

    # limpando excel
    def excel_clean(self, **kwargs):

        # carregando excel
        workbook = ol.load_workbook(filename=self.excel_path, keep_vba=True)

        # selecionando sheet
        sh1 = workbook['Monthly']

        # deletando linhas inúteis
        sh1.delete_rows(1, 2)
        sh1.delete_rows(3)

        # salvando workbook limpo
        workbook.save(rf'{self.save_path}/excel_cleaned_{self.today}.xlsx')

        return self

    # carregando csv
    def load_csv(self, **kwargs):
        # carregando excel limpo
        df_santander = pd.read_excel(rf'{self.save_path}/excel_cleaned_{self.today}.xlsx', sheet_name='Monthly')

        # copiando primeira linha para coluna
        df_santander.columns = df_santander.iloc[0]

        # dropando primeira linha
        self.df_santander = df_santander.drop(0)

        # definindo logging de aviso                  
        self.lm.logger_warning_limit(self.df_santander, 'SANTANDER', 348)

        # definindo logging de erro                  
        self.lm.logger_error_cols(self.df_santander, 'SANTANDER', 22)

    # renomeando colunas do csv
    def rename_columns_csv(self, **kwargs):
        # velhas colunas
        cols_old = ['date', 'IGP-M_percentual', 'IPCA_percentual', 'INPC_percentual','INCC_percentual', 
                    'IGP-M_acumulated', 'IPCA_acumulated', 'INPC_acumulated', 'INCC_acumulated',
                    'BRL/USD - end of period', 'BRL/USD - month average',
                    'USD/EUR - final', 'Selic target',
                    'Effective selic annualized_percentual', 'Effective monthly CDI_percentual',
                    'TJLP', 'TLP', "IBGE's unemployment_percentual",
                    "IBGE's unemployment (s.a.)", 'FED Funds',
                    'Libor 12m (average) / SOFR', 'CDS Brazil 5Y']

        # snakecase function
        snakecase = lambda x: inflection.underscore( x )

        # novas colunas no snakecase
        cols_new = map( snakecase, cols_old)

        # passando novas colunas
        self.df_santander.columns = cols_new

    # mudando dtypes
    def changing_dtypes(self, **kwargs):
        # copying dataframe
        df_santander = self.df_santander.copy()

        # mudando os "-" para "0"
        df_santander.iloc[:,1:] = df_santander.iloc[:,1:].apply(lambda x: x.replace('-', '0'))
                                
        # mudando de string para float
        self.df_santander.iloc[:,1:] = df_santander.iloc[:,1:].astype(float)