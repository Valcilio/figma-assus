import os
from pandas.testing import assert_frame_equal
import pytest

from cryptocurrencyetl import CryptocurrencyEtl

crypto = 'BTC'
market_curr = 'USD'
api_key = os.environ.get('TOKEN_FIGMA_CRYPTO_KEY')
crypt_etl = CryptocurrencyEtl(crypto=crypto, market_curr=market_curr, api_key=api_key)

class TestCryptoEtl():

    def test_data_extract_shape(self):

        df = crypt_etl.extract_cryptocurrency_data()

        assert df.shape[1] == 11

    def test_clean_cryptocurrency_data(self):

        df = crypt_etl.clean_cryptocurrency_data()

        assert df.shape == (1000, 6)
        
    def test_datetimeindex(self):

        df = crypt_etl.change_to_datetime_index()
        df['test'] = 1
        df = df['test'].reset_index().select_dtypes('datetime64[ns]')
        dateindex_check = df.shape[1]

        assert dateindex_check == 1