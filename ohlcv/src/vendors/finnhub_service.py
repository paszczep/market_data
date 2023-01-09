import finnhub
from finnhub.exceptions import FinnhubAPIException
from typing import Callable
from os import environ
import time
from ohlcv.src.utility.in_and_out import load_env_variables, \
    config, write_rows_to_file_and_db, timestamp_to_datetime, get_last_open_time, split_time, get_base_dir
import logging

load_env_variables()

api_key = environ['finnhub_API_Key']

finnhub_client = finnhub.Client(api_key=api_key)

time_bar = config.time_bar


def get_crypto_symbols() -> dict:
    crypto_symbols = finnhub_client.crypto_symbols('BINANCE')
    symbols = {element['displaySymbol']: element['symbol'] for element in crypto_symbols}
    return symbols


def api_except(func: Callable, *args) -> dict:
    try:
        candles = func(*args)
        return candles
    except FinnhubAPIException as api_exception:
        logging.info(f'API error symbol: {api_exception}')
        if api_exception.status_code == 429:
            time.sleep(60)


def get_stock_candles(symbol: str, from_timestamp: int, to_timestamp: int):
    stock_candles = api_except(finnhub_client.stock_candles, symbol, '5', from_timestamp, to_timestamp)
    return stock_candles


def get_crypto_candles(symbol: str, from_timestamp: int, to_timestamp: int):
    symbol = f'BINANCE:{symbol}'
    crypto_candles = api_except(finnhub_client.crypto_candles, symbol, '5', from_timestamp, to_timestamp)
    return crypto_candles


def debug_dict(record_dict: dict) -> dict:
    record_dict['t'] = timestamp_to_datetime(record_dict['t'])
    record_dict['debug'] = {'created': timestamp_to_datetime(int(time.time()))}
    return record_dict


record_keys = list('tohlcv')


def unwind_records(records_dict: dict, symbol: str, ticker_type: str):
    elements = range(len(records_dict['t']))
    record_dicts = [{key: records_dict[key][index] for key in record_keys} for index in elements]
    logging.info(f'{ticker_type} {symbol} {len(record_dicts)} rows')
    if len(record_dicts) > 1:
        # Drop inconclusive record
        record_open_time = record_dicts[-1]['t']
        if record_open_time > int(time.mktime(time.gmtime()) - time_bar):
            record_dicts.pop(-1)
    columns = record_keys.copy()
    if config.debug:
        record_dicts = [debug_dict(record_dict) for record_dict in record_dicts]
        columns.append('debug')

    write_rows_to_file_and_db(
        symbol=symbol,
        rows=record_dicts,
        columns=columns,
        source=f'finnhub_{ticker_type}')


def run_finnhub_tickers(end_timestamp: int, ticker_type: str, ticker_func: Callable, ticker_list: list):

    for symbol in ticker_list:
        designator = f'{ticker_type}_{symbol}'
        last_open_time = get_last_open_time(vendor=(vendor := 'finnhub'), symbol=designator)
        start_timestamp = last_open_time + time_bar
        if start_timestamp < end_timestamp - config.time_bar:
            time_sections = split_time(start=start_timestamp, end=end_timestamp)
            for time_section in time_sections:
                section_start = time_section[0]
                section_end = time_section[1]
                logging.info(f'getting {designator} from {vendor} '
                             f'start: {timestamp_to_datetime(section_start)} '
                             f'end: {timestamp_to_datetime(section_end)}')
                candles = ticker_func(
                    symbol=symbol,
                    from_timestamp=section_start,
                    to_timestamp=section_end)
                if candles:
                    if candles['s'] == 'ok':
                        unwind_records(records_dict=candles, symbol=symbol, ticker_type=ticker_type)
                    if candles['s'] == 'no_data':
                        logging.info(f"no data on {ticker_type} {symbol}")


def run_finnhub_crypto_tickers(end_timestamp: int):
    run_finnhub_tickers(
        end_timestamp=end_timestamp,
        ticker_type='crypto',
        ticker_func=get_crypto_candles,
        ticker_list=config.crypto_tickers
    )


def run_finnhub_stock_tickers(end_timestamp: int):
    run_finnhub_tickers(
        end_timestamp=end_timestamp,
        ticker_type='stock',
        ticker_func=get_stock_candles,
        ticker_list=config.stock_symbols
    )


if __name__ == '__main__':
    time = int(time.time() - 30000)
    time_ago = time - 300000
    test_candles = get_stock_candles('GOOGL', time_ago, time)
    print(test_candles)
