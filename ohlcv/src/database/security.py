import csv
import json
from datetime import datetime


class BinanceOHLCV:
    def __init__(self, row):
        self.timestamp = row['open_time']
        self.open_price = row['open_price']
        self.high_price = row['high_price']
        self.low_price = row['low_price']
        self.close_price = row['close_price']
        self.volume = row['volume']

    def __dict__(self):
        row = {
            'timestamp': self.timestamp,
            'open': self.open_price,
            'high': self.high_price,
            'low': self.low_price,
            'close': self.close_price,
            'volume': self.volume}
        return row


class FinnhubOHLCV:
    def __init__(self, row):
        self.timestamp = row['t']
        self.open_price = row['o']
        self.high_price = row['h']
        self.low_price = row['l']
        self.close_price = row['c']
        self.volume = row['v']

    def __dict__(self):
        row = {
            'timestamp': self.timestamp,
            'open': self.open_price,
            'high': self.high_price,
            'low': self.low_price,
            'close': self.close_price,
            'volume': self.volume
        }
        return row


class Security:
    def __init__(self, file):
        ticker_info = file.stem.split('_')

        exchange = ticker_info[0]
        ticker_type = ticker_info[1]
        ticker_symbol = ticker_info[2]
        open_file = open(file, 'r')
        reader = csv.DictReader(open_file, delimiter=';')

        ohlcv_row = {
            'binance': BinanceOHLCV,
            'finnhub': FinnhubOHLCV}

        rows = [ohlcv_row[exchange](line).__dict__() for line in reader]

        self.ticker = f'{exchange}:{ticker_symbol}'
        self.symbol = ticker_type
        self.name = ticker_symbol
        self.isin = 'foo'
        self.conid = 'bar'
        self.exchange = exchange
        self.last_record = datetime.fromtimestamp(int(rows[-1]['timestamp']))
        self.listed = False
        self.status_history = json.dumps('foo-bar')
        self.updated = str(datetime.now())
        self.transfer_algotrader = False
        self.ohlcv = json.dumps(rows)


class Exchange:
    def __init__(self, file):
        name = file.stem.split('_')[0]
        self.code = name
        self.name = name
        self.timezone = 'UTC'
        self.properties = json.dumps('')
        self.trading_session = json.dumps('')
