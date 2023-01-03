import sched
import time
import logging
from typing import Callable, Union
import sys
from pathlib import Path
path_to_append = str(Path.cwd().parent)
sys.path.append(path_to_append)
from ohlcv.src.utility.in_and_out import config, timestamp_to_datetime
from ohlcv.src.vendors.binance_service import run_tickers_binance
from ohlcv.src.vendors.finnhub_service import run_finnhub_crypto_tickers, run_finnhub_stock_tickers


run_until = config.run_until
ticker_list = config.crypto_tickers
time_bar = config.time_bar


def time_bar_time(timestamp: Union[int, float]) -> int:
    timestamp = int((timestamp // time_bar) * time_bar)
    return timestamp


def time_bar_time_ago(timestamp: Union[int, float]) -> int:
    timestamp = int((timestamp // time_bar) * time_bar) - time_bar
    return timestamp


def time_bar_ago(timestamp: Union[int, float]) -> int:
    timestamp = int(timestamp) - time_bar
    return timestamp


def run_scheduled_vendor(func: Callable, func_time: Callable):
    scheduler = sched.scheduler(time.time, time.sleep)
    proc_time = time.time()
    while proc_time < run_until + time_bar:
        grid_time = time_bar_time(proc_time)
        logging.info(f'scheduled next grab for {timestamp_to_datetime(grid_time)}')
        kwargs = {'end_timestamp': func_time(proc_time)}
        scheduler.enterabs(proc_time, 0, func, kwargs=kwargs)
        proc_time = grid_time + time_bar
        scheduler.run()


def run_scheduled_binance():
    run_scheduled_vendor(run_tickers_binance, time_bar_ago)


def run_scheduled_finnhub_crypto():
    run_scheduled_vendor(run_finnhub_crypto_tickers, time_bar_time)


def run_scheduled_finnhub_stock():
    run_scheduled_vendor(run_finnhub_stock_tickers, time_bar_time)

