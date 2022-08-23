"""Сheck postgress database availability."""

import psycopg2
from core.config import settings
from utils.backoff import backoff

pg_settings = {
    'dbname': settings.postgres.dbname,
    'user': settings.postgres.user,
    'password': settings.postgres.password,
    'host': settings.postgres.host,
    'port': settings.postgres.port,
    'connect_timeout': settings.postgres.connect_timeout,
}


@backoff()
def pg_connect():
    """Wait for Postrgress."""
    connection = psycopg2.connect(**pg_settings)
    connection.close()


if __name__ == '__main__':
    pg_connect()
