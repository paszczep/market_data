import logging
import time
from binance import Client
from os import environ
from ohlcv.src.utility.in_and_out import config, load_env_variables, timestamp_to_datetime

load_env_variables()
API_Key = environ['BINANCE_KEY']
API_Secret = environ['BINANCE_SECRET']


def get_client(key: str = API_Key, secret: str = API_Secret, test: bool = config.testnet) -> Client:
    try:
        global_client = Client(key, secret, testnet=test)
    except ConnectionError as connection_error:
        retry_seconds = 10
        logging.info(f"connection error {connection_error}. retrying in {str(retry_seconds)}")
        time.sleep(retry_seconds)
        global_client = get_client()
    return global_client


def debug_dict(kline_dict: dict) -> dict:
    for key, value in kline_dict.items():
        if '_time' in key:
            kline_dict[key] = timestamp_to_datetime(value / 1000)
        if key == 'unused':
            kline_dict[key] = {'created': timestamp_to_datetime(int(time.time()))}
    return kline_dict


def test_connection():
    test_client = get_client()
    assert test_client.ping() == {}


def get_all_available_tickers(all_tickers_client: Client = get_client()) -> list:
    available_info = all_tickers_client.get_all_tickers()
    all_tickers_list = [element['symbol'] for element in available_info]
    return all_tickers_list


def get_server_time(server_time_client: Client) -> int:
    time_res = server_time_client.get_server_time()
    return time_res['serverTime']


def server_system_maintenance(status_client: Client) -> bool:
    status = status_client.get_system_status()
    maintenance = bool(status['status'])
    return maintenance


def get_symbol_info(symbol: str, symbol_client: Client):
    info = symbol_client.get_symbol_info(symbol)
    return info


def get_average_price(symbol: str, symbol_client: Client):
    avg_price = symbol_client.get_avg_price(symbol=symbol)
    return avg_price

