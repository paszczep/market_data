from ohlcv.src.database.insert_into_db import insert_security_to_db
from ohlcv.src.database.security import Exchange
import json
from csv import DictWriter
from pathlib import Path
from datetime import datetime
from typing import List, Dict, TextIO, Tuple
import logging
import dotenv


def get_base_dir() -> Path:
    base_dir = Path(__file__).parent.parent.parent.parent
    logging.info(f"getting base directory at {base_dir}")
    return base_dir


def get_config_file_path() -> Path:
    base_dir = get_base_dir()
    config_json_file_path = base_dir / 'ohlcv' / 'config.json'
    logging.info(f"getting config file at {config_json_file_path.resolve()}")
    return config_json_file_path


def read_config() -> dict:
    config_json_file_path = get_config_file_path()
    config_json_file = open(config_json_file_path, 'r')
    config_dict = json.load(config_json_file)
    return config_dict


class Config:
    def __init__(self):
        config_source = read_config()
        self.time_bar = 300
        self.datetime_format = config_source['datetime_format']
        self.run_until = config_source['run_until']
        self.historic_range = config_source['historic_range']
        self.testnet = config_source['testnet']
        self.debug = config_source['debug']
        self.value_labels = config_source['value_labels']
        self.crypto_tickers = config_source['crypto_tickers']
        self.stock_symbols = config_source['stock_symbols']

    def update_config_file(self):
        config_json_file_path = get_config_file_path()
        config_file = open(config_json_file_path, 'w')
        config_values = self.__dict__
        json.dump(config_values, config_file)


def get_output_dir() -> Path:
    base_dir = get_base_dir()
    output_directory = base_dir / 'output'
    Path.mkdir(output_directory, exist_ok=True)
    return output_directory


output_dir = get_output_dir()


def get_output_file(vendor: str, symbol: str, output_path: Path = output_dir) -> Path:
    file_name = Path(f'{vendor}_{symbol}.csv')
    file_path = output_path / file_name
    return file_path


def open_output_file(file_path: Path):
    open_file = open(file_path, 'a', newline='')
    return open_file


def get_csv_dict_writer_and_file(vendor: str, symbol: str, columns: list) -> Tuple[DictWriter, TextIO]:
    file_path = get_output_file(vendor, symbol)
    isfile = Path.is_file(file_path)
    csv_file = open_output_file(file_path)
    dict_writer = DictWriter(csv_file, fieldnames=columns, delimiter=';')
    if not isfile:
        logging.info(f"created file {file_path.name}")
        dict_writer.writeheader()
    return dict_writer, csv_file


def write_rows_to_file_and_db(source: str, symbol: str, columns: list, rows: List[Dict]):
    writer, file = get_csv_dict_writer_and_file(
        vendor=source,
        symbol=symbol,
        columns=columns
    )
    for row in rows:
        writer.writerow(row)

    file.close()

    security_file = get_output_file(vendor=source, symbol=symbol)

    if security_file.is_file():
        insert_security_to_db(security_file)


config = Config()
DATETIME_STR_FORMAT = config.datetime_format


def timestamp_to_datetime(timestamp: int) -> str:
    timestamp = datetime.fromtimestamp(timestamp)
    datetime_string = timestamp.strftime(DATETIME_STR_FORMAT)
    return datetime_string


def timestamp_from_string(datetime_string: str) -> int:
    try:
        timestamp = int(datetime_string)
    except ValueError:
        timestamp = int(datetime.timestamp(datetime.strptime(datetime_string, DATETIME_STR_FORMAT)))
    return timestamp


def get_last_open_time(vendor: str, symbol: str):
    """read last saved record open time to que requests for missing elements"""
    output_file = get_output_file(vendor=vendor, symbol=symbol)
    if not Path.is_file(output_file):
        return config.historic_range
    csv_file = open(output_file, 'r')
    data = csv_file.readlines()
    last_time = data[-1].split(';')[0]
    last_time = timestamp_from_string(last_time)
    return last_time


def split_time(start: int, end: int) -> list:
    max_row_number = 1000
    time_bar = config.time_bar
    req_time = time_bar * max_row_number
    time_frame = (end - start)
    sections = range(time_frame // req_time)
    reminder = time_frame % req_time
    even_times = [(start + section*req_time, start + (section + 1)*req_time) for section in sections]
    times = even_times + [(end - reminder, end)]
    return times


def update_tickers_and_symbols():
    folder = get_base_dir()
    crypto_file = folder / 'input' / 'all_crypto_tickers.csv'
    # stock_file = folder / 'input' / 'working_stock_symbols.csv'
    read = open(crypto_file, 'r').read().splitlines()
    # config.stock_symbols = read
    config.crypto_tickers = read
    config.update_config_file()


def insert_exchanges_str(exchange: Exchange) -> str:
    insert_str = f"""
    INSERT INTO exchanges 
    (code, name, timezone, properties, trading_session)
    VALUES
    ('{exchange.code}', '{exchange.name}', '{exchange.timezone}', '{exchange.properties}', '{exchange.trading_session}')
    """
    return insert_str
