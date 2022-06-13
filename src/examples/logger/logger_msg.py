import datetime as dt
import logging
from pandas.core.frame import DataFrame

class LoggerMSG():

    def __init__(self, **kwargs):
        
        # dia atual
        self.today = dt.datetime.now().strftime('%Y%m%d%H')

        # configurando o log
        logging.basicConfig(
            filename=f'../logs/log_{self.today}.txt',
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.DEBUG
            )

        self.logger = logging.getLogger('financial_etl')

    def logger_warning_limit(self, df: DataFrame, nome: str, limit: int, **kwargs):
        if df.shape[0] < limit:
            self.logger.warning(f'''Está sendo extraído menos informações do {nome}
                                 do que o esperado!''')
                
            raise Warning(f'''Está sendo extraído menos informações do {nome}
                                 do que o esperado!''')

    def logger_error_cols(self, df: DataFrame, nome: str, limit: int, **kwargs):
        if df.shape[1] != limit:
            self.logger.error(f'''Está sendo extraído uma quantidade diferente de colunas
                            do {nome} do que o esperado!''')
                
            raise ValueError(f'''Está sendo extraído uma quantidade diferente de colunas
                            do {nome} do que o esperado!''')