import datetime as dt
import logging
from pandas.core.frame import DataFrame

class LoggerMsg():

    def __init__(self, file_name: str, **kwargs):
        
        # dia atual
        self.today = dt.datetime.now().strftime('%Y%m%d%H%M%S')

        # configurando o log
        logging.basicConfig(
            filename=f'../logs/log_{self.today}.txt',
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.DEBUG
            )

        self.logger = logging.getLogger(file_name)

    def full_warning(self, msg: str, **kwargs):

        self.logger.info(msg)

        return Warning(msg)

    def full_error(self, msg: str, **kwargs):

        self.logger.info(msg)

        raise ValueError(msg)

    def init_extract(self, name: str, **kwargs):

        msg = f'''Initing extract of {name}!'''
        self.logger.info(msg)

        return Warning(msg)

    def init_data_transform(self, name: str, **kwargs):

        msg = f'''Initing data transform of {name}!'''
        self.logger.info(msg)

        return Warning(msg)

    def generic_error(self, name: str, **kwargs):

        msg = f'''Generic error in {name}, check the code!'''
        self.logger.error(msg)

        raise ValueError(msg)

    def warning_limit_rows(self, df: DataFrame, name: str, limit: int, **kwargs):
        if df.shape[0] != limit:

            msg = f'''Extracting less rows from {name} than waited ({limit} != {df.shape[0]})!'''
            self.logger.warning(msg)
            
            return Warning(msg)

    def error_limit_cols(self, df: DataFrame, name: str, limit: int, **kwargs):
        if df.shape[1] != limit:

            msg = f'''Extracting diferent quantity of columns from {name} than expected ({limit} != {df.shape[1]})!'''
            self.logger.error(msg)

            raise ValueError(msg)

    def end_msg(self, name: str, **kwargs):

        msg = f'''{name} finished!'''
        self.logger.info(msg)

        return msg