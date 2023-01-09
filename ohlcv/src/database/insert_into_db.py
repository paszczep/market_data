from ohlcv.src.database.security import Security, Exchange
from ohlcv.src.database.connect import db_cursor, db_connection, DB_EXCHANGES, DB_SECURITIES
import logging
from pathlib import Path

existing_exchanges = DB_EXCHANGES
existing_securities = DB_SECURITIES


def update_ohlcv_in_db_query(security: Security) -> str:
    update_str = f"""
    UPDATE securities
    SET
    ohlcv='{security.ohlcv}',
    last_record='{security.last_record}',
    updated='{security.updated}'
    WHERE
    ticker='{security.ticker}'
    """
    return update_str


def create_insert_security_query(security: Security) -> str:
    insert_str = f"""
        INSERT INTO securities
        (ticker, symbol, name, isin, conid, exchange, last_record, listed,
        status_history, updated, transfer_algotrader, ohlcv)
        VALUES
        ('{security.ticker}', '{security.symbol}', '{security.name}', '{security.isin}',
        '{security.conid}', '{security.exchange}', '{security.last_record}', '{security.listed}',
        '{security.status_history}', '{security.updated}', '{security.transfer_algotrader}', '{security.ohlcv}');
        """
    return insert_str


def insert_exchanges_str(exchange: Exchange) -> str:
    insert_str = f"""
    INSERT INTO exchanges 
    (code, name, timezone, properties, trading_session)
    VALUES
    ('{exchange.code}', '{exchange.name}', '{exchange.timezone}', '{exchange.properties}', '{exchange.trading_session}')
    """
    return insert_str


def insert_security_to_db(file: Path):
    security = Security(file)
    connection = db_connection()
    cursor = db_cursor(connection)
    if security.ticker not in existing_securities:
        insert_query = create_insert_security_query(security)
        logging.info(f'inserting {security.ticker} into database')
        cursor.execute(insert_query)
        existing_securities.append(security.ticker)
    else:
        update_query = update_ohlcv_in_db_query(security)
        logging.info(f'updating {security.ticker} in database')
        cursor.execute(update_query)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    pass
