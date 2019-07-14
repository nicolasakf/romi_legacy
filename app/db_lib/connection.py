import mysql.connector
import pandas as pd

HOST = 'localhost'
USER = 'root'
PWD = 'F1nt5yn6!'

# HOST = '3.217.217.48'
# USER = 'romi'
# PWD = 'romiconnect'


def _init_connection(host=HOST, user=USER, password=PWD):

    _conn = mysql.connector.connect(
        use_pure=False,
        host=host,
        user=user,
        password=password,
    )
    _cursor = _conn.cursor()

    return _conn, _cursor


def select(query, **kwargs):

    _conn, _ = _init_connection(**kwargs)
    _df = pd.read_sql(query, con=_conn)
    _conn.close()

    return _df


def insert(query, values=None, **kwargs):

    _conn, _cursor = _init_connection(**kwargs)
    if values is None:  _cursor.execute(query)
    else:  _cursor.executemany(query, values)
    _conn.commit()
    _conn.close()
