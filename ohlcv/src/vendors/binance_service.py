from typing import List, Dict
from ohlcv.src.utility.in_and_out import write_rows_to_file_and_db, config, \
    timestamp_to_datetime, get_last_open_time, split_time
from ohlcv.src.vendors.binance_utility import debug_dict, Client, get_client
import logging
import time
from datetime import timedelta


def run_tickers_binance(end_timestamp: int):
    ticker_list = config.crypto_tickers
    tickers_client = get_client()
    logging.info(f"starting all {str(len(ticker_list))} tickers at "
                 f"{timestamp_to_datetime(int(start := time.time()))}")
    for ticker in ticker_list:
        write_data_row(
            symbol=ticker,
            writing_client=tickers_client,
            end_timestamp=end_timestamp
        )
    logging.info(f"ending all tickers"
                 f" - elapsed {timedelta(seconds=(time.time() - start))}")


def normalise_row_timestamps(row_dict: dict) -> dict:
    for key, value in row_dict.items():
        if '_time' in key:
            row_dict[key] = int(value / 1000)
    return row_dict


def get_5min_kline(symbol: str,
                   start_timestamp: int,
                   end_timestamp: int,
                   klines_client: Client) -> List[Dict]:

    klines = klines_client.get_klines(
        symbol=symbol,
        startTime=start_timestamp * 1000,
        endTime=end_timestamp * 1000,
        interval=Client.KLINE_INTERVAL_5MINUTE,
        limit=1000)

    kline_dicts = [dict(zip(config.value_labels, kline)) for kline in klines]
    logging.info(f'{symbol} {len(kline_dicts)} rows')
    if config.debug:
        kline_dicts = [debug_dict(kline_dict) for kline_dict in kline_dicts]
    else:
        kline_dicts = [normalise_row_timestamps(kline_dict) for kline_dict in kline_dicts]
    return kline_dicts


def write_data_row(
        symbol: str,
        end_timestamp: int,
        writing_client: Client):
    source = 'binance_crypto'
    start_timestamp = get_last_open_time(vendor=source, symbol=symbol)
    if start_timestamp < end_timestamp - config.time_bar:
        time_sections = split_time(start=start_timestamp, end=end_timestamp)
        for time_section in time_sections:
            start = time_section[0]
            end = time_section[1]
            logging.info(f'getting {symbol} from binance '
                         f'start: {timestamp_to_datetime(start)}, '
                         f'end: {timestamp_to_datetime(end)}.')
            rows = get_5min_kline(
                symbol=symbol,
                klines_client=writing_client,
                start_timestamp=start + config.time_bar,
                end_timestamp=end)
            if len(rows) > 0:
                write_rows_to_file_and_db(source=source, symbol=symbol, rows=rows, columns=config.value_labels)


if __name__ == '__main__':
    pass
