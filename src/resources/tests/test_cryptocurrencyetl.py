import os
from random import choice
import sys
sys.path.insert(0, os.environ.get('SRC_FIGMA_PATH'))

from cryptocurrencyetl import CryptocurrencyEtl

crypto = choice(('BTC', 'ETH', 'ADA', 'DOGE', 'XRP'))
market_curr = choice(('USD', 'BRL', 'CNY', 'EUR', 'GBP'))
api_key = os.environ.get('TOKEN_FIGMA_CRYPTO_KEY')
crypt_etl = CryptocurrencyEtl(crypto=crypto, market_curr=market_curr, api_key=api_key)


def test_data_extract_shape():

    df = crypt_etl.extract_cryptocurrency_data()

    assert df.shape[1] == 11

def test_clean_cryptocurrency_data():

    df = crypt_etl.clean_cryptocurrency_data()

    assert df.shape[1] == 6

def test_datetimeindex():

    df = crypt_etl.change_to_datetime_index()
    df['test'] = 1
    df = df['test'].reset_index().select_dtypes('datetime64[ns]')
    dateindex_check = df.shape[1]

    assert dateindex_check == 1