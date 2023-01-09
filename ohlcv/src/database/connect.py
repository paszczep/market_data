import psycopg2

POSTGRES_DB = 'keiser'
POSTGRES_USER = 'henswurst'
POSTGRES_PASSWORD = 'password1234'
HOST = 'database'
# HOST = 'localhost'


def db_connection():
    connection = psycopg2.connect(
        host=HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
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
