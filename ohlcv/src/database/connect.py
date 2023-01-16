import psycopg2
from os import environ
from pathlib import Path
import logging
import dotenv


def get_base_dir() -> Path:
    base_dir = Path(__file__).parent.parent.parent.parent
    logging.info(f"getting base directory at {base_dir}")
    return base_dir


def load_env_variables():
    dotenv_file_path_str = get_base_dir() / 'ohlcv' / '.env'
    dotenv.load_dotenv(dotenv_file_path_str.resolve())


load_env_variables()


def db_connection():
    connection = psycopg2.connect(
        host=environ['HOST'],
        database=environ['POSTGRES_DB'],
        user=environ['POSTGRES_USER'],
        password=environ['POSTGRES_PASSWORD']
    )

    return connection


def db_cursor(connection):
    cursor = connection.cursor()
    return cursor


def retereive_existing(select_statement: str) -> list:
    db_con = db_connection()
    cursor = db_cursor(db_con)
    cursor.execute(select_statement)
    data = [el[0] for el in cursor.fetchall()]
    return data


def existing_exchanges() -> list:
    exchanges_data = retereive_existing("SELECT code FROM exchanges")
    return exchanges_data


DB_EXCHANGES = existing_exchanges()


def existing_securities() -> list:
    securities_data = retereive_existing("SELECT ticker FROM securities")
    return securities_data


DB_SECURITIES = existing_securities()
