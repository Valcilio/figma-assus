import datetime as dt
from pickle import FALSE
import pandas as pd

from resources.logger.logger_msg import LoggerMsg

class CryptocurrencyEtl():

    def __init__(self, api_key: str, crypto: str, market_curr: str, **kwargs):

        self.api_key = api_key
        self.crypto = crypto
        self.market_curr = market_curr
        self.logger = LoggerMsg(file_name='Cryptocurrency ETL')

    def extract_cryptocurrency_data(self, activate_errors_msg = True, **kwargs):

        self.logger.init_extract(name=f'ETL to obtain {self.crypto} historical data in {self.market_curr} value')
        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={self.crypto}&market={self.market_curr}&apikey={self.api_key}&datatype=csv'
        df = pd.read_csv(url)
        self.df = df.copy()

        if activate_errors_msg:
            self.logger.warning_limit_rows(df=self.df, name=f'Alpha Vantage API', limit=1000)
            self.logger.error_limit_cols(df=self.df, name=f'Alpha Vantage API', limit=11)

        return df

    def clean_cryptocurrency_data(self, **kwargs):

        self.logger.init_data_transform(name=f'{self.crypto} historical data')
        df = self.df.copy()
        market_curr = self.market_curr

        cols = ['timestamp', f'open ({market_curr})', f'high ({market_curr})', 
                f'low ({market_curr})', f'close ({market_curr})', 'volume']
        
        name_cols = {f'open ({market_curr})':'open', f'high ({market_curr})':'high', 
                    f'low ({market_curr})':'low', f'close ({market_curr})':'close'}

        try:
            df1 = df[cols].rename(columns=name_cols)

        except:
            self.logger.generic_error(name='Data Transform')

        self.df = df1.copy()

    def change_to_datetime_index(self, **kwargs):

        df = self.df.copy()
        df = df.set_index('timestamp').sort_index()
        df.index = pd.to_datetime(df.index)
        self.df = df.copy()

    def test_market_curr(self, **kwargs):

        some_market_currencies_codes = ['USD', 'BRL', 'CNY', 'EUR', 'GBP']
        backup_market_curr = self.market_curr

        for mcc in some_market_currencies_codes:

            self.market_curr = mcc

            try:
                self.run()
                self.logger.end_msg(name='test')

            except:
                self.logger.generic_error("ETL's test")

        self.market_curr = backup_market_curr

    def test_crypto(self, **kwargs):

        some_cryptocurrencies_codes = ['BTC', 'ETH', 'ADA', 'DOGE', 'XRP']
        backup_crypto = self.crypto

        for ccc in some_cryptocurrencies_codes:

            self.crypto = ccc

            try:
                self.run()
                self.logger.end_msg(name='test')

            except:
                self.logger.generic_error("ETL's test")

        self.crypto = backup_crypto

    def run(self, **kwargs):

        self.df = self.extract_cryptocurrency_data()
        self.clean_cryptocurrency_data()
        self.change_to_datetime_index()
        self.logger.end_msg(name=f'ETL')

        return self.df