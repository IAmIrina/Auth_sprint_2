"""Project settings."""

from datetime import timedelta

from pydantic import BaseSettings, Field


class DotEnvMixin(BaseSettings):
    class Config:
        env_file = '.env'


class RedisSettings(DotEnvMixin):
    """Redis connection settings."""
    host: str = Field('127.0.0.1', env='REDIS_HOST')
    port: int = Field(6379, env='REDIS_PORT')
    password: str = Field('f73rt6r3etfr3rtw5r35t', env='REDIS_PASSWORD')


class TestRedisSettings(DotEnvMixin):
    """Redis connection settings."""
    host: str = Field('127.0.0.1', env='TEST_REDIS_HOST')
    port: int = Field(6379, env='TEST_REDIS_PORT')
    password: str = Field('f73rt6r3etfr3rtw5r35t', env='TEST_REDIS_PASSWORD')


class PostgresSettings(DotEnvMixin):
    """Postgres connection settings."""

    host: str = Field('127.0.0.1', env='POSTGRES_HOST')
    port: int = Field(5432, env='POSTGRES_PORT')
    dbname: str = Field('auth_movies', env='POSTGRES_AUTH_DB')
    user: str = Field(env='POSTGRES_USER')
    password: str = Field(env='POSTGRES_PASSWORD')
    connect_timeout: int = 1


class TestPostgresSettings(DotEnvMixin):
    """Postgres connection settings."""

    host: str = Field('127.0.0.2', env='TEST_POSTGRES_HOST')
    port: int = Field(5432, env='TEST_POSTGRES_PORT')
    dbname: str = Field('auth_movies', env='TEST_POSTGRES_AUTH_DB')
    user: str = Field(env='TEST_POSTGRES_USER')
    password: str = Field(env='TEST_POSTGRES_PASSWORD')
    connect_timeout: int = 1


class Settings(DotEnvMixin):

    redis: RedisSettings = RedisSettings()
    test_redis: TestRedisSettings = TestRedisSettings()
    postgres: PostgresSettings = PostgresSettings()
    test_postgres: TestPostgresSettings = TestPostgresSettings()
    port: int = Field(9001, env='AUTH_API_PORT')
    host: str = Field('0.0.0.0', env='AUTH_API_HOST')
    jwt_secret_key = Field('Some-secret-key')
    jwt_access_token_expires = Field(timedelta(minutes=30))
    jwt_refresh_token_expires = Field(timedelta(days=10))


settings = Settings()
