import psycopg2
from psycopg2.errors import UniqueViolation

POSTGRES_DB = 'keiser'
POSTGRES_USER = 'henswurst'
POSTGRES_PASSWORD = 'password1234'
HOST = 'localhost'


def db_connection():
    connection = psycopg2.connect(
        host=HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD)

    return connection


DB_CONNECTION = db_connection()


def db_cursor(connection=DB_CONNECTION):
    cursor = connection.cursor()
    return cursor


def row_exists_exception(func_first, func_second, *kwargs):
    try:
        func_first(*kwargs)
    except UniqueViolation:
        func_second(*kwargs)


def write_to_file(string):
    text_file = open("query.txt", "w")
    text_file.write(string)
    text_file.close()


def retereive_existing(select_statement: str) -> list:
    cursor = db_cursor()
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
