import datetime as dt
import pandas as pd
from logger.logger_msg import LoggerMSG  

  
class BacenETL(LoggerMSG):

    def __init__(self, **kwargs):
        self.today = dt.datetime.now().strftime('%Y%m%d%H')
        self.lm = LoggerMSG()

    def run(self, **kwargs):
        # chamando métodos
        self.extract_bacen()
        self.data_ajusts()

        return self.df_bacen

    # extraindo dados do BACEN
    def extract_bacen(self, **kwargs):
        # extraindo dados do BACEN
        df_pib = self.consulta_bc(22099)

        # renomeando colunas
        df_pib = df_pib.rename(columns={'valor':'pib_monthly', 'data':'date'})

        # extraindo dados do BACEN e salvando no dataframe
        df_pib['pib_agro_monthly'] = self.consulta_bc(22083)['valor']

        # extraindo dados do BACEN e salvando no dataframe
        df_pib['pib_indus_monthly'] = self.consulta_bc(22084)['valor']

        # extraindo dados do BACEN e salvando no dataframe
        df_pib['pib_serv_monthly'] = self.consulta_bc(22089)['valor']

        # extraindo dados do BACEN e salvando no dataframe
        df_pib['consumo_familiar_monthly'] = self.consulta_bc(22100)['valor']

        # salvando self
        self.df_pib = df_pib.copy()

        # definindo logging de aviso                  
        self.lm.logger_warning_limit(self.df_pib, 'PIB', 107)

        # extraindo dados do BACEN
        df_ipca = self.consulta_bc(1635)

        # renomeando colunas
        self.df_ipca = df_ipca.rename(columns={'valor':'ipca_alimentos_percentual_monthly', 'data':'date'})

        # definindo logging de aviso                  
        self.lm.logger_warning_limit(self.df_ipca, 'IPCA', 369)

        # rodando método
        self.data_ajusts()

        return self

    def data_ajusts(self, **kwargs):
        # copiando dataframes
        df_pib = self.df_pib.copy()
        df_ipca = self.df_ipca.copy()
        
        # derivando variáveis de tempo
        df_pib['month'] = df_pib['date'].dt.month
        df_pib['year'] = df_pib['date'].dt.year

        # desenvolvendo variável de tempo referência
        df_ref = df_ipca['date'].copy().reset_index()

        # derivando variáveis de tempo no ref
        df_ref['month'] = df_ref['date'].dt.month
        df_ref['year'] = df_ref['date'].dt.year

        # dropping index
        df_ref = df_ref.drop('index', axis=1)

        # juntando dataframe
        df_merge = pd.merge(df_ref, df_pib, how='left', on=['month', 'year'])

        # juntando dados
        df_merge = df_merge.drop('date_y', axis=1).rename(columns={'date_x':'date'})

        # preenchendo NAs com os valores anteriores
        df_merge = df_merge.fillna(method='ffill')

        # tirando preenchimentos errôneos
        df_merge.iloc[-1, 3:] = None

        # juntando com a tabel de IPCA
        self.df_bacen = pd.merge(df_merge, df_ipca, how='left', on='date')

        # definindo logging de erro                  
        self.lm.logger_error_cols(self.df_bacen, 'BACEN', 9)

        return self.df_bacen

    # função de extração de dados da API do BACEN
    def consulta_bc(self, codigo_bcb, **kwargs):
        url = rf'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb}/dados?formato=json'
        df_bacen = pd.read_json(url)
        df_bacen['data'] = pd.to_datetime(df_bacen['data'], dayfirst=True)
        return df_bacen