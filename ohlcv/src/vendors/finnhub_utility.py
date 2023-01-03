import finnhub
from finnhub_service import finnhub_client, get_base_dir, write_rows_to_file


def get_crypto_profile(symbol: str, finnhub_client: finnhub.Client = finnhub_client):
    """premium only"""
    crypto_profile = finnhub_client.crypto_profile(symbol)
    return crypto_profile


def get_crypto_exchanges(finnhub_client: finnhub.Client = finnhub_client) -> list:
    crypto_exchanges = finnhub_client.crypto_exchanges()
    return crypto_exchanges


def get_crypto_symbols(finnhub_client: finnhub.Client = finnhub_client):
    symbols = finnhub_client.crypto_symbols('BINANCE')
    return symbols


def get_stock_symbols(finnhub_client: finnhub.Client = finnhub_client):
    stock_symbols = finnhub_client.stock_symbols('US')
    return stock_symbols


def lookup_stock():
    file = get_base_dir() / 'input' / 'stock_searches.txt'

    lines = open(file, 'r').read().splitlines()
    rows = []
    for line in lines:
        results = finnhub_client.symbol_lookup(line)
        if results['count'] > 0:
            row = {key: value for key, value in results['result'][0].items()}
            row['search'] = line
            rows.append(row)

    keys = ['search', 'description', 'displaySymbol', 'symbol', 'type', 'primary']
    write_rows_to_file(
        source='finnhub',
        symbol='symbol_lookup',
        columns=keys,
        rows=rows,
    )


if __name__ == '__main__':

    pass
