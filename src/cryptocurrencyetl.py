import pandas as pd

from resources.logger_msg import LoggerMsg

class CryptocurrencyEtl():

    def __init__(self, api_key: str, crypto: str, market_curr: str, **kwargs):

        self.api_key = api_key
        self.crypto = crypto
        self.market_curr = market_curr

        self.orig_cols = ['timestamp', f'open ({self.market_curr})', f'high ({self.market_curr})', 
                          f'low ({self.market_curr})', f'close ({self.market_curr})', 'volume']

        self.logger = LoggerMsg(file_name='CryptoETL')

    def extract_cryptocurrency_data(self, activate_errors_msg = True, **kwargs):
        '''Extract the cryptocurrency historical data from the API selected and
        check if has the quantity of rows and cols correct to go for the next step.'''

        self.logger.init_extract(name=f'ETL to obtain {self.crypto} historical data in {self.market_curr} value')
        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={self.crypto}&market={self.market_curr}&apikey={self.api_key}&datatype=csv'
        self.df = pd.read_csv(url)

        if activate_errors_msg:
            self.logger.warning_limit_rows(df=self.df, name=f'Alpha Vantage API', limit=1000)
            self.logger.error_limit_cols(df=self.df, name=f'Alpha Vantage API', limit=11)

        return self.df

    def clean_cryptocurrency_data(self, **kwargs):
        '''Filter the dataframe to just contain the important columns to procedure
        with the next steps'''

        self.logger.init_data_transform(name=f'{self.crypto} historical data')
        self.df = self.df[self.orig_cols]

        return self.df

    def rename_columns(self, **kwargs):
        '''Rename columns to a default name for future process'''

        name_cols = {f'open ({self.market_curr})':'open', f'high ({self.market_curr})':'high', 
                    f'low ({self.market_curr})':'low', f'close ({self.market_curr})':'close'}
        try:
            self.df = self.df.rename(columns=name_cols)
        except:
            self.logger.generic_error(name='Data Transform')

        return self.df

    def change_to_datetime_index(self, **kwargs):
        '''Change set timestamp column to the index and change it into datetimeindex'''

        self.df = self.df.set_index('timestamp').sort_index()
        self.df.index = pd.to_datetime(self.df.index)

        return self.df

    def test_market_curr(self, **kwargs):
        '''Test the market_curr codes who will be in the final software'''

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
        '''Test cryptocurrency codes who will be in the final software'''

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
        '''Run all the ETL'''

        self.extract_cryptocurrency_data()
        self.clean_cryptocurrency_data()
        self.rename_columns()
        self.change_to_datetime_index()
        self.logger.end_msg(name=f'ETL')

        return self.df