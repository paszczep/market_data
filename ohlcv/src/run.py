import sys
from pathlib import Path
path_to_append = str(Path.cwd().parent)
sys.path.append(path_to_append)
from ohlcv.src.utility.in_and_out import timestamp_to_datetime, config
from ohlcv.src.utility.schedule import run_scheduled_binance, run_scheduled_finnhub_crypto, run_scheduled_finnhub_stock
import logging
from multiprocessing import Process


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s: %(message)s',
    force=True
)


if __name__ == '__main__':
    logging.info("running application")
    logging.info(f'run until {timestamp_to_datetime(config.run_until)}')
    logging.info(f'fetch data from {timestamp_to_datetime(config.historic_range)}')

    process_binance = Process(target=run_scheduled_binance)
    process_binance.start()

    process_finnhub_stock = Process(target=run_scheduled_finnhub_stock)
    process_finnhub_stock.start()

    process_finnhub_crypto = Process(target=run_scheduled_finnhub_crypto)
    process_finnhub_crypto.start()

    process_finnhub_crypto.join()
    process_binance.join()
    process_finnhub_stock.join()
