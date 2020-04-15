from urllib.parse import urlparse

from flask import current_app, g
from psycopg2.extras import DictCursor
from psycopg2.pool import SimpleConnectionPool


def init_app(app):
    app.teardown_appcontext(close_db)


def get_conn():
    """
    return created database connection object
    if not exist create new database connection object
    :return: database
    """
    if 'conn_pool' not in g:
        result = urlparse(current_app.config['DATABASE_URL'])
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname

        g.conn_pool = SimpleConnectionPool(
            1, 5, host=hostname,
            database=database,
            user=username,
            password=password
        )

    return g.conn_pool.getconn()


def put_conn(conn):
    if 'conn_pool' in g:
        g.conn_pool.putconn(conn)


def close_db(e=None):
    conn_pool = g.pop('conn_pool', None)

    if conn_pool is not None:
        conn_pool.closeall()


def execute(query, values):
    conn = get_conn()

    try:
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
    finally:
        put_conn(conn)


def query_one(query, values):
    conn = get_conn()

    try:
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute(query, values)
        result = cur.fetchone()
    finally:
        put_conn(conn)

    return result


def query_all(query, values):
    conn = get_conn()

    try:
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute(query, values)
        result = cur.fetchall()
    finally:
        put_conn(conn)

    return result
