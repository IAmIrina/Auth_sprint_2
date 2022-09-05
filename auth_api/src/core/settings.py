"""Project settings."""

from datetime import timedelta

from pydantic import BaseSettings, Field


class DotEnvMixin(BaseSettings):
    class Config:
        env_file = '.env'


class RedisSettings(DotEnvMixin):
    """Redis connection settings."""
    host: str = '127.0.0.1'
    port: int = 6379
    password: str = 'f73rt6r3etfr3rtw5r35t'


class PostgresSettings(DotEnvMixin):
    """Postgres connection settings."""

    host: str = '127.0.0.1'
    port: int = 5432
    dbname: str = 'auth_movies'
    user: str
    password: str
    connect_timeout: int = 1


class OauthServiceProvider(DotEnvMixin):
    client_id: str
    client_secret: str
    access_token_url: str
    access_token_params: str = None
    authorize_url: str
    authorize_params: str = None
    api_base_url: str = None
    userinfo_endpoint: str
    token_endpoint_auth_method: str = 'client_secret_basic'
    client_kwargs: dict


def get_params(cls, env_prefix_name: str):
    class Params(cls):
        class Config:
            env_prefix = f'{env_prefix_name}_'
    return Params()


class Settings(DotEnvMixin):

    redis: RedisSettings = get_params(RedisSettings, 'redis')
    test_redis: RedisSettings = get_params(RedisSettings, 'test_redis')
    postgres: PostgresSettings = get_params(PostgresSettings, 'postgres')
    test_postgres: PostgresSettings = get_params(PostgresSettings, 'test_postgres')
    port: int = Field(9001, env='AUTH_API_PORT')
    host: str = Field('0.0.0.0', env='AUTH_API_HOST')
    jwt_secret_key = Field('Some-secret-key')
    jwt_access_token_expires = Field(timedelta(minutes=30))
    jwt_refresh_token_expires = Field(timedelta(days=10))

    secret_key: str

    google: OauthServiceProvider = get_params(OauthServiceProvider, 'google')
    vk: OauthServiceProvider = get_params(OauthServiceProvider, 'vk')
    mail: OauthServiceProvider = get_params(OauthServiceProvider, 'mail')
    yandex: OauthServiceProvider = get_params(OauthServiceProvider, 'yandex')


settings = Settings()
