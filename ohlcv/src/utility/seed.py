import psycopg2

POSTGRES_DB = 'keiser'
POSTGRES_USER = 'henswurst'
POSTGRES_PASSWORD = 'password1234'
HOST = 'localhost'


def get_connection_and_cursor():
    returned_connection = psycopg2.connect(
        host=HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD)

    returned_cursor = returned_connection.cursor()
    return returned_connection, returned_cursor


def insert_seed_vendors():

    query_string = """
    INSERT INTO exchanges 
    (code, name, timezone, properties, trading_session)
    VALUES
    ('finnhub', 'finnhub', 'UTC', '["json"]', '["json"]'),
    ('binance', 'binance', 'UTC', '["json"]', '["json"]');
    """

    connection, cursor = get_connection_and_cursor()
    cursor.execute(query_string)
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    print('')
