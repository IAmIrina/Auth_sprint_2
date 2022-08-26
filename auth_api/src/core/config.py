from core.settings import settings


class DefaultConfig():
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = settings.secret_key
    JWT_SECRET_KEY = settings.jwt_secret_key
    JWT_ACCESS_TOKEN_EXPIRES = settings.jwt_access_token_expires
    JWT_REFRESH_TOKEN_EXPIRES = settings.jwt_refresh_token_expires
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(
        user=settings.postgres.user,
        password=settings.postgres.password,
        host=settings.postgres.host,
        port=settings.postgres.port,
        db_name=settings.postgres.dbname,
    )
    VK_CLIENT_ID = settings.vk_client_id
    VK_CLIENT_SECRET = settings.vk_client_secret
    GOOGLE_CLIENT_ID = settings.google_client_id
    GOOGLE_CLIENT_SECRET = settings.google_client_secret

    PAGINATE_PAGE_SIZE = 50
    PAGINATE_PAGE_PARAM = "page"
    PAGINATE_SIZE_PARAM = "size"
    PAGINATE_RESOURCE_LINKS_ENABLED = False
    PAGINATE_DATA_OBJECT_KEY = "results"
    PAGINATE_PAGINATION_OBJECT_KEY = False
    CACHE_HOST = settings.redis.host
    CACHE_PORT = settings.redis.port
    CACHE_PASSWORD = settings.redis.password


class TestingConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(
        user=settings.test_postgres.user,
        password=settings.test_postgres.password,
        host=settings.test_postgres.host,
        port=settings.test_postgres.port,
        db_name=settings.test_postgres.dbname,
    )
    CACHE_HOST = settings.test_redis.host
    CACHE_PORT = settings.test_redis.port
    CACHE_PASSWORD = settings.test_redis.password
    DEBUG = True
    TESTING = True
