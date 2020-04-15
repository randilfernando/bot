from urllib.parse import urlparse

import psycopg2
from flask import current_app, g


def init_app(app):
    app.teardown_appcontext(close_db)


def get_db():
    """
    return created database connection object
    if not exist create new database connection object
    :return: database
    """
    if 'db' not in g:
        result = urlparse(current_app.config['DATABASE_URL'])
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname

        g.db = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
